from django.views.generic import ListView, DetailView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from apps.main.models import Category, Product
from apps.main.serializers import ProductSerializer


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


class ProductApi(ListModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
