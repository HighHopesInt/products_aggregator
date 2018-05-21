from django.shortcuts import render
from django.views.generic import ListView
from _apps.main.models import Category, Product

# Create your views here.


# not working yet
class CatalogTree(ListView):
    template_name = 'catalog.html'

    def get_queryset(self):
        filter = self.kwargs['filter']

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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(CatalogTree, self).get_context_data(**kwargs)
    #     # context['nodes'] = Category.objects.all()


def catalog_tree(request, filter=None):

    if filter:
        cat = Category.objects.get(
            name=filter
        )
        categories = cat.get_descendants(include_self=True).all().values_list('id', flat=True)
        product_list = Product.objects.all().filter(category_id__in=categories)
    else:
        product_list = []

    context = {
        'nodes': Category.objects.all(),
        'product_list': product_list,
    }
    return render(request, 'catalog.html', context)
