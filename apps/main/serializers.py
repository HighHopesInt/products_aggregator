from rest_framework import serializers

from apps.main.models import Product


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
                  'size',
                  'url',
                  'image_url',
                  'free_shipping',
                  'available',
                  'price',
                  'sale_price',)
