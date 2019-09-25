from django_filters import rest_framework as filtres
from django.views.generic import ListView, DetailView
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.generics import get_object_or_404

from apps.main.models import (Category, Product, Color, Brand,
                              Gender, Retailer)
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


class ProductFilter(filtres.FilterSet):
    min_price = filtres.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filtres.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['title',
                  'brand', 'retailer', 'color',
                  'material', 'available',
                  'min_price', 'max_price',
                  'size']


class ProductApi(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = (filtres.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        color = get_object_or_404(Color, id=self.request.data.get('color_id'))
        brand = get_object_or_404(Brand, id=self.request.data.get('brand_id'))
        gender = get_object_or_404(Gender,
                                   id=self.request.data.get('gender_id'))
        retailer = get_object_or_404(Retailer,
                                     id=self.request.data.get('retailer_id'))
        return serializer.save(color=color,
                               brand=brand,
                               gender=gender,
                               retailer=retailer)


class SingleProductAPI(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
