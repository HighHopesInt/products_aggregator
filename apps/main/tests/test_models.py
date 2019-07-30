from django.test import TestCase
from apps.main.models import Product, Category


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(description='Example description',
                               meta_description='Meta desc',
                               short_description='Short desc',
                               title='It is title',
                               meta_title='It is title',
                               material='Plastic',
                               size='45 EU',
                               free_shipping=True,
                               available=False,
                               price=45.6)

    def test_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_description_lenght(self):
        prodcut = Product.objects.get(id=1)
        max_length = prodcut._meta.get_field('name').max_length
        self.assertEquals(max_length, 1000)


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Dona')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_name_unique(self):
        category = Category.objects.get(id=1)
        unique = category._meta.get_field('name').unique
        self.assertEquals(unique, True)
