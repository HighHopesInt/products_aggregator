from django.test import TestCase
from apps.main.models import Product, Category, Brand


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Dona')
        brand = Brand.objects.create()
        Product.objects.create(category=category,
                               brand=brand,
                               description='Example description',
                               meta_description='Meta desc',
                               short_description='Short desc',
                               title='It is title',
                               meta_title='It is title',
                               material='Plastic',
                               size='45 EU',
                               free_shipping=True,
                               available=False,
                               price=45.6,
                               gender='Women')

    def test_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_description_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('description').max_length
        self.assertEquals(max_length, 1000)

    def test_meta_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('meta_description').verbose_name
        self.assertEquals(field_label, 'meta description')

    def test_meta_description_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('meta_description').max_length
        self.assertEquals(max_length, 500)

    def test_short_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('short_description').verbose_name
        self.assertEquals(field_label, 'short description')

    def test_short_description_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('short_description').max_length
        self.assertEquals(max_length, 500)

    def test_title_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('title').max_length
        self.assertEquals(max_length, 500)

    def test_material_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('material').verbose_name
        self.assertEquals(field_label, 'material')

    def test_material_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('material').max_length
        self.assertEquals(max_length, 50)

    def test_gender_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('gender').verbose_name
        self.assertEquals(field_label, 'gender')

    def test_gender_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('gender').max_length
        self.assertEquals(max_length, 5)

    def test_size_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('size').verbose_name
        self.assertEquals(field_label, 'size')

    def test_size_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('size').max_length
        self.assertEquals(max_length, 100)

    def test_url_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('url').verbose_name
        self.assertEquals(field_label, 'url')

    def test_image_url_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('image_url').verbose_name
        self.assertEquals(field_label, 'image url')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field('price').verbose_name
        self.assertEquals(max_digits, 'price')

    def test_price_max_digits(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').max_digits
        self.assertEquals(field_label, 16)

    def test_sale_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('sale_price').verbose_name
        self.assertEquals(field_label, 'sale price')

    def test_sale_price_max_digits(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field('sale_price').max_digits
        self.assertEquals(max_digits, 16)

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
