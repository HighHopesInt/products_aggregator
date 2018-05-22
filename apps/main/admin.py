from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, Brand, Color, Retailer, UploadedFiles

# Register your models here.


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name',)


# class UploadedFilesAdmin(admin.ModelAdmin):
# #     name = forms.CharField()
# #     file = forms.FileField(
# #         label='Select a file'
# #     )
#
#     def save_model(self, request, obj, form, change):
#         for afile in request.FILES.getlist('files_multiple'):
#             obj.photos.create(image=afile)


admin.site.register([Product, Brand, Color, Retailer])
admin.site.register(Category, CategoryAdmin)

admin.site.register(UploadedFiles)
