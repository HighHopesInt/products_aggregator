from django.shortcuts import render
from django.db.models import Count

from apps.main.models import Product, Brand


def stats(request):
    count = Product.objects.all().count()
    top_brand = (Brand.objects.all().annotate(num=Count('products'))
                 .order_by('-num').values_list('name', 'num'))[:5]
    top_male_boot = (Product.objects.filter(gender='Men').order_by('-price')
                     .values_list('title', 'brand__name', 'color__name',
                                  'price', 'sale_price').distinct())[:3]
    top_female_boot = (Product.objects.filter(gender='Women')
                       .order_by('-price')
                       .values_list('title', 'brand__name', 'color__name',
                                    'price', 'sale_price').distinct())[:3]
    context = {
        'count': count,
        'top_brand': top_brand,
        'top_male_boot': top_male_boot,
        'top_female_boot': top_female_boot
    }
    return render(request, 'stats.html', context)
