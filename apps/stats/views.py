from django.shortcuts import render
from django.db.models import Count

from apps.main.models import Product, Brand


def stats(request):
    count = Product.objects.all().count()
    top_brand = (Brand.objects.all().annotate(num=Count('products'))
                 .order_by('-num').values_list('name', 'num'))[:5]
    context = {
        'count': count,
        'top_brand': top_brand,
    }
    return render(request, 'stats.html', context)
