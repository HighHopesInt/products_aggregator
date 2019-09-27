from rest_framework import serializers

from apps.main.models import Product, UploadedFile


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',
                  'category',
                  'description',
                  'meta_description',
                  'short_description',
                  'title',
                  'meta_title',
                  'retailer',
                  'brand',
                  'color',
                  'material',
                  'gender',
                  'eu_size',
                  'us_size',
                  'url',
                  'image_url',
                  'free_shipping',
                  'available',
                  'price',
                  'sale_price',)


class UploadFileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id',
                  'file',)
