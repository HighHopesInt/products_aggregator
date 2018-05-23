from django.views.generic import ListView, DetailView
from apps.main.models import Category, Product


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
            product_list = Product.objects.all().filter(
                category_id__in=categories)
        else:
            product_list = []

        return product_list


class ProductView(DetailView):
    template_name = "product.html"
    model = Product
