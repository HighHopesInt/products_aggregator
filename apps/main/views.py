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

    # it works, but moved to context processors
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductList, self).get_context_data(**kwargs)
    #     context['category_tree'] = Category.objects.all()
    #     return context


class ProductView(DetailView):
    template_name = "product.html"
    model = Product
