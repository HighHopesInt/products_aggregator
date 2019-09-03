from django.shortcuts import render
from django.db.models import Count, FloatField
from django.db.models.functions import Cast

from apps.main.models import Product, Brand, Color


def stats(request):
    count = Product.objects.all().count()
    top_brand = (Brand.objects.annotate(num=Count('products'))
                 .order_by('-num').values_list('name', 'num'))[:5]
    top_male_boot = (Product.objects.filter(gender='Men').order_by('-price')
                     .values_list('title', 'brand__name', 'color__name',
                                  'price', 'sale_price').distinct())[:3]
    top_female_boot = (Product.objects.filter(gender='Women')
                       .order_by('-price')
                       .values_list('title', 'brand__name', 'color__name',
                                    'price', 'sale_price').distinct())[:3]
    per_ratio = (Color.objects.annotate(
                 num=Cast(Count('product') / count * 100, FloatField()))
                 .order_by('name').values_list('name', 'num'))
    famous_stat = (Product.objects.filter(description__icontains='Famous')
                   .count())
    ret_stat = (Product.objects.values('retailer').
                annotate(prod_of=Count('id'),
                         brand_of=Count('brand', distinct=True))
                .values_list('retailer__name', 'brand_of', 'prod_of'))
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
