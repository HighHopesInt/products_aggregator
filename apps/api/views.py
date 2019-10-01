from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


from apps.main.models import (Category, Product, Color, Brand,
                              Retailer, UploadedFile)
from apps.api import serializers


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    eu_size = filters.NumberFilter(field_name='size',
                                   method='eu_size_method',
                                   label='EU Size')
    us_size = filters.NumberFilter(field_name='size',
                                   method='us_size_method',
                                   label='Us Size')

    def eu_size_method(self, queryset, name, value):
        return (queryset.filter(size__gte=24).filter(size__icontains=value))

    def us_size_method(self, queryset, name, value):
        return (queryset.filter(size__gte=8).filter(size__icontains=value))

    class Meta:
        model = Product
        fields = [
            'title',
            'brand', 'retailer', 'color',
            'material', 'available',
            'min_price', 'max_price',
            'eu_size', 'us_size',
        ]


class ProductApi(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def perform_create(self, serializer):
        category = get_object_or_404(Category,
                                     id=self.request.data.get('category'))
        color = get_object_or_404(Color, id=self.request.data.get('color'))
        brand = get_object_or_404(Brand, id=self.request.data.get('brand'))
        retailer = get_object_or_404(Retailer,
                                     id=self.request.data.get('retailer'))
        return serializer.save(category=category,
                               color=color,
                               brand=brand,
                               retailer=retailer)


class SingleProductAPI(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class FileUploadApi(ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = serializers.UploadFileSerialzer
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def perform_create(self, serializer):
        return serializer.save()
