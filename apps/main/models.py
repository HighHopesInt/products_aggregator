from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

Gender = (
    ('men', 'Men'),
    ('women', 'Women'),
)


class Category(MPTTModel):

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.full_name

    name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        db_index=True
    )


@receiver(pre_save, sender=Category)
def set_full_name(sender, instance, *args, **kwargs):
    if not instance.full_name:
        instance.full_name = instance.name


class Product(models.Model):

    def __str__(self):
        return self.short_description

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    description = models.CharField(max_length=1000, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)
    short_description = models.CharField(max_length=100)

    title = models.CharField(max_length=100, blank=True)
    meta_title = models.CharField(max_length=100, blank=True)

    retailer = models.ForeignKey('Retailer', null=True,
                                 on_delete=models.SET_NULL,
                                 blank=True)

    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    color = models.ForeignKey('Color', null=True,
                              on_delete=models.SET_NULL,
                              blank=True)
    material = models.CharField(max_length=50, blank=True)

    gender = models.CharField(max_length=5, choices=Gender)

    size = models.CharField(max_length=100, blank=True)

    url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)

    free_shipping = models.BooleanField()
    available = models.BooleanField()

    price = models.DecimalField(max_digits=16, decimal_places=2, blank=True)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2,
                                     blank=True)


class Retailer(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
