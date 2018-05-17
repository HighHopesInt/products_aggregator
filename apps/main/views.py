from django.shortcuts import render
from apps.main.models import Category, Product

# Create your views here.


def catalog_tree(request, filter=None):

    if filter:
        cat = Category.objects.get(
            name=filter
        )
        categories = cat.get_descendants(include_self=True).all()
        product_list = Product.objects.all().filter(category__in=categories)
    else:
        product_list = []

    return render(request, 'catalog.html',
                  {
                      'nodes': Category.objects.all(),
                      'product_list': product_list,
                   }
                  )
