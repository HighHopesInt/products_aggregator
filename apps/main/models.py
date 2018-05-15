from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

Gender = (
    ('men', 'Men'),
    ('women', 'Women'),
)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        db_index=True
    )


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    description = models.CharField(max_length=1000)
    meta_description = models.CharField(max_length=500)
    short_description = models.CharField(max_length=100)

    title = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)

    retailer = models.ForeignKey('Retailer', null=True,
                                 on_delete=models.SET_NULL)

    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    color = models.ForeignKey('Color', null=True,
                              on_delete=models.SET_NULL)
    material = models.CharField(max_length=50)

    gender = models.CharField(max_length=5, choices=Gender)

    size = models.CharField(max_length=100)

    url = models.URLField()
    image_url = models.URLField()

    free_shipping = models.BooleanField()
    available = models.BooleanField()

    price = models.DecimalField(max_digits=16, decimal_places=2)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2)


class Retailer(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
