from django.shortcuts import render
from django.db.models import Count, FloatField
from django.db.models.functions import Cast

from apps.main.models import Product, Brand, Color, Retailer


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
    per_ratio = (Color.objects.all().annotate(
                 num=Cast(Count('product') / count * 100, FloatField()))
                 .order_by('name').values_list('name', 'num'))
    famous_stat = (Product.objects.filter(description__icontains='Famous')
                   .count())
    ret_stat = (Retailer.objects.all().annotate(prod_of=Count('product'))
                .values_list('name', 'brand_of', 'prod_of'))
    context = {
        'count': count,
        'top_brand': top_brand,
        'top_male_boot': top_male_boot,
        'top_female_boot': top_female_boot,
        'per_ratio': per_ratio,
        'famous_word': famous_stat,
        'retailer_stat': ret_stat,
    }
    return render(request, 'stats.html', context)
