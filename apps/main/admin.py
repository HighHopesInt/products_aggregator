from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, Brand, Color

# Register your models here.


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name',)


admin.site.register([Product, Brand, Color])
admin.site.register(Category, CategoryAdmin)
