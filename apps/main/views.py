from django_filters import rest_framework as filters
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


from apps.main.models import (Category, Product, Color, Brand,
                              Retailer, UploadedFile)
from apps.main import serializers


class ProductList(ListView):
    template_name = 'catalog.html'

    def get_queryset(self):
        filter = self.kwargs.get('filter', None)

        if filter:
            cat = Category.objects.get(
                name=filter
            )
            categories = cat.get_descendants(
                include_self=True).all().values_list('id', flat=True)

            if self.request.GET.get('checkbox', default=False):
                product_list = Product.objects.all().filter(
                        category_id__in=categories, available=True)
                self.save = True
            else:
                product_list = Product.objects.all().filter(
                        category_id__in=categories)
        else:
            product_list = []

        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.GET.get('checkbox', default=False):
            context['save'] = True
        else:
            context['save'] = False
        return context


class ProductView(DetailView):
    template_name = "product.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data()
        context['exist_image'] = False
        context['size_str'] = context['object'].size_format()
        if context['object'].image_exists():
            context['exist_image'] = True
        return context


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
