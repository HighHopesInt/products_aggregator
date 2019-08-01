from django.test import TestCase
from django.urls import reverse
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
