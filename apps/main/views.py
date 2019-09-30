from django_filters import rest_framework as filtres
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions


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


class ProductFilter(filtres.FilterSet):
    min_price = filtres.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filtres.NumberFilter(field_name='price', lookup_expr='lte')
    eu_size = filtres.NumberFilter(field_name='size',
                                   method='eu_size_method',
                                   label='EU Size')
    us_size = filtres.NumberFilter(field_name='size',
                                   method='eu_size_method',
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
    filter_backends = (filtres.DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]


class FileUploadApi(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        files = UploadedFile.objects.all()
        serializer = serializers.UploadFileSerialzer(files, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        file_serializer = serializers.UploadFileSerialzer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
