from django.contrib import admin

from .models import Category, Product, Brand, Color

# Register your models here.

admin.site.register([Category, Product, Brand, Color])
