#!/usr/bin/env python3
import csv, sys, os

DIR = '/home/wis/projects/rik/core'

FILE_NAME = '/home/wis/projects/rik/stuff/WOMEN_SHOES.csv'

sys.path.append(DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django

django.setup()

import apps.main.models as models
from django.core.exceptions import ObjectDoesNotExist


def get_category(name, parent=None):
    cat, _ = models.Category.objects.get_or_create(name=name,
                                                         parent=parent)
    return cat


def get_brand(name):
    brand, _ = models.Brand.objects.get_or_create(name=name)
    return brand


def get_color(name):
    color, created = models.Color.objects.get_or_create(name=name)
    return color


def get_retailer(name):
    retailer, created = models.Retailer.objects.get_or_create(name=name)
    return retailer


first = True

reader = csv.DictReader(open(FILE_NAME))
reader.fieldnames = [name.lower() for name in reader.fieldnames]
for row in reader:
    # this code needs improvement
    try:
        product = models.Product.objects.get(
            url=row['url']
        )
    except ObjectDoesNotExist:
        pass
    else:
        print(product, ' already exists, passed.')
        continue

    product = models.Product()
    product.url = row['url']
    product.gender = row['gender']

    cats = list()
    cat_fields = ['gender', 'main category', 'subcategory', 'subsubcategory']

    for i, name in enumerate(cat_fields):
        parent = None if i == 0 else cats[i-1]
        csv_value = row[name]

        cats.append(get_category(csv_value, parent))

    product.category = next(i for i in cats[::-1] if i)

    product.brand = get_brand(row['brand'])
    product.color = get_color(row['color'])

    product.size = row['size']
    product.material = row['material']

    product.description = row['description']
    product.short_description = row['short description']
    product.meta_description = row['meta description']
    product.title = row['title']
    product.meta_title = row['meta title']

    product.retailer = get_retailer(row['retailer name'])

    product.image_url = row['image url']
    product.free_shipping = bool(row['free shipping'])
    product.available = bool(row['available'])
    product.price = row['price']
    product.sale_price = row['sale price']

    product.save()

    print(product, ' created.')

    first = False

    # if not first:
    #     break

print('Successfully loaded.')