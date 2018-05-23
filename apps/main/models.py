from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

Gender = (
    ('men', 'Men'),
    ('women', 'Women'),
)

Status = (
    ('SUCCESS', 'Success'),
    ('ERROR', 'Error'),
)


class BaseAttributesModel(models.Model):
    """Common settings. """

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, unique=True)


class Category(MPTTModel):

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        db_index=True
    )


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

    price = models.DecimalField(max_digits=16, decimal_places=2,
                                null=True, blank=True, default=0)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2,
                                     null=True, blank=True, default=0)


class Retailer(BaseAttributesModel):
    pass


class Brand(BaseAttributesModel):
    pass


class Color(BaseAttributesModel):
    pass


class UploadedFile(BaseAttributesModel):
    class Meta:
        verbose_name_plural = 'Uploaded files'

    NONE = "N"
    PENDING = "P"
    BEGIN = "B"
    SUCCESS = "S"
    ERROR = "E"
    ALMOST = "A"

    STATUS_CHOICES = (
        (NONE, 'None'),
        (PENDING, 'Pending'),
        (BEGIN, 'Begin'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
        (ALMOST, 'Almost')
    )

    # name = models.CharField(max_length=256, unique=True)
    file = models.FileField(upload_to='uploaded_files')

    status = models.CharField(max_length=20, blank=True,
                              choices=STATUS_CHOICES, default=NONE)
    log = models.TextField(default='', blank=True)

    def update_status(self, status, log=""):
        self.status = status
        self.log += log

        fields = ['status', 'log'] if log else ['status']
        self.save(update_fields=fields)