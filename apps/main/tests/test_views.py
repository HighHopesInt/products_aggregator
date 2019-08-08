import os
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from mixer.backend.django import mixer


from apps.main.models import UploadedFile, Product, Category
from apps.main.admin import UploadedFileAdmin


class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Women')
        for item in range(15):
            mixer.blend(Product, category=category)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)

    def test_view_index_url_accessible_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalog.html')


class TestUploadFile(TestCase):

    class MockSuperUser:
        def has_perm(self, perm):
            return True

        def is_active(self):
            return True

        def is_staff(self):
            return True

        def get_group_permissions(self):
            return ('main.add_uploadedfile', )

    request_factory = RequestFactory()
    request = request_factory.get('/admin')
    request.user = MockSuperUser()
    request.files = [os.path.abspath('apps/main/tests/test_files/sample.csv'),
                     os.path.abspath('apps/main/tests/test_files/file.txt')]

    def setUp(self):
        site = AdminSite()
        self.admin = UploadedFileAdmin(UploadedFile, site)

    def test_upload_status_code(self):
        proceed = self.admin.multiple_upload_files(self.request)
        self.assertEquals(proceed.status_code, 200)

    def test_upload_files(self):
        print(self.request.files[0])
        for item in self.request.files:
            with open(item) as f:
                self.client.post('/admin/main/uploadedfile/add/', {'form': f})


class PermissionTest(TestCase):

    def setUp(self):
        self.client = Client()

        group_supervisers, created_s = \
            Group.objects.get_or_create(name='Admin')
        group_admins, created_a = \
            Group.objects.get_or_create(name='Supervisers')
        group_managers, created_m = \
            Group.objects.get_or_create(name='Managers')

        ct = ContentType.objects.get_for_model(UploadedFile)
        permission_change_file = Permission.objects.create(
            codename='main.change_uploadedfile',
            name='Can change uploadedfile',
            content_type=ct
        )
        permission_add_file = Permission.objects.create(
            codename='main.add_uploadedfile',
            name='Can add upload file',
            content_type=ct
        )

        group_supervisers.permissions.add(permission_change_file)
        group_admins.permissions.add(permission_add_file)
        group_managers.permissions.add(permission_add_file)

        test_supervisor = User.objects.create_user(username='Supervisor',
                                                   password='12345678')
        test_admin = User.objects.create_user(username='Admin',
                                              password='12345678')
        test_manager = User.objects.create_user(username='Manager',
                                                password='12345678')

        test_supervisor.save()
        test_admin.save()
        test_manager.save()

        test_supervisor.groups.add(group_supervisers)
        test_admin.groups.add(group_admins)
        test_manager.groups.add(group_managers)

    def test_add_upload_file_for_supervisers(self):
        self.client.login(username='Supervisor', password='12345678')
        resp = self.client.get('/admin/main/uploadedfile/add/')
        self.assertEquals(resp.status_code, 302)

    def test_add_upload_file_for_admin(self):
        self.client.login(username='Admin', password='12345678')
        resp = self.client.get('/admin/main/uploadedfile/add/', follow=True)
        self.assertEquals(resp.status_code, 200)

    def test_add_upload_file_for_manager(self):
        self.client.login(username='Manager', password='12345678')
        resp = self.client.get('/admin/main/uploadedfile/add/', follow=True)
        self.assertEquals(resp.status_code, 200)
