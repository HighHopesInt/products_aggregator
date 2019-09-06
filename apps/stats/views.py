from django.shortcuts import render
from django.db.models import Count, FloatField, ExpressionWrapper

from apps.main.models import Product


def stats(request):
    products_count = Product.objects.all().count()
    top_brand = (Product.objects.values('brand')
                 .annotate(num=Count('title'))
                 .order_by('-num').values_list('brand__name', 'num'))[:5]
    top_male_boot = (Product.objects.filter(gender__iexact='men')
                     .order_by('-price')
                     .values_list('title', 'brand__name', 'color__name',
                                  'price', 'sale_price', 'id')
                     .distinct())[:3]
    top_female_boot = (Product.objects.filter(gender__iexact='women')
                       .order_by('-price')
                       .values_list('title', 'brand__name', 'color__name',
                                    'price', 'sale_price', 'id')
                       .distinct())[:3]
    per_ratio = (Product.objects.values('color').annotate(
                    num=ExpressionWrapper(
                        Count('title') * 100 / float(products_count),
                        output_field=FloatField()))
                 .values_list('color__name', 'num').order_by('-num'))
    other_percent = [percent[1] for percent in per_ratio
                     if not isinstance(percent[1], type(None))
                     and percent[1] < 1.0]
    other_percent = round(sum(other_percent), 4)
    famous_stat = (Product.objects.filter(description__icontains='famous')
                   .count())
    ret_stat = (Product.objects.values('retailer').
                annotate(prod_of=Count('id'),
                         brand_of=Count('brand', distinct=True))
                .order_by('retailer__name')
                .values_list('retailer__name', 'brand_of', 'prod_of'))
    print(type(top_female_boot))
    context = {
        'count': products_count,
        'top_brand': top_brand,
        'top_male_boot': top_male_boot,
        'top_female_boot': top_female_boot,
        'per_ratio': per_ratio,
        'famous_word': famous_stat,
        'retailer_stat': ret_stat,
        'other_percent': other_percent,
    }
    return render(request, 'stats.html', context)
