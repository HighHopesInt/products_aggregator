from django.test import TestCase
from mixer.backend.django import mixer
from apps.main.models import Product, UploadedFile


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        mixer.blend(Product, image_url='http://google.com')
        mixer.blend(Product, image_url=('https://hsto.org'
                                        '/files/839/634/9c3/'
                                        '8396349c3e804e45833b14213ed0efd3'
                                        '.png'))

    def test_exist_image(self):
        product_without_image = Product.objects.get(id=1)
        product_with_image = Product.objects.get(id=2)
        self.assertEquals(product_without_image.image_exists(), False)
        self.assertEquals(product_with_image.image_exists(), True)


class UploadedFileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        mixer.blend(UploadedFile, file='/apps/main/tests/test_files/'
                                       'sample.csv')

    def test_create_name(self):
        file = UploadedFile.objects.get(id=1)
        self.assertEquals(file.name, 'apps/main/tests/test_files/sample.csv')
