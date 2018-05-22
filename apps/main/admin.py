from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Brand, Color, Retailer, UploadedFile


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)

admin.site.register([Product, Brand, Color, Retailer])

admin.site.register(UploadedFile)
