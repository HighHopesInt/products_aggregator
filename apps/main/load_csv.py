import csv

from django.core.exceptions import ObjectDoesNotExist

from apps.main.models import *


def parse(datafile_instance):

    datafile_instance.update_status(UploadedFile.PENDING)

    reader = csv.DictReader(open(datafile_instance.file.path))
    reader.fieldnames = [name.lower() for name in reader.fieldnames]

    required_fields = {'url', 'short description', 'gender', 'main category'}

    fields_not_in_file = required_fields - set(reader.fieldnames)
    if fields_not_in_file:
        datafile_instance.update_status(
            UploadedFile.ERROR,
            'Not valid file! Required fields: {}'.format(
                ', '.join(fields_not_in_file)
            )
        )
    else:
        datafile_instance.update_status(UploadedFile.BEGIN)
        skipped_empty = 0

        for row in reader:

            empty_values = [i for i in required_fields if not row[i].strip()]
            if empty_values:
                skipped_empty += 1

                log_string = 'Skipped line #{}, empty fields: {}\n'.format(
                    reader.line_num,
                    ', '.join(empty_values)
                )
                datafile_instance.log += log_string
                datafile_instance.save(update_fields=['log'])
                continue

            try:
                product = Product.objects.get(
                    url=row['url']
                )
            except ObjectDoesNotExist:
                pass
            else:
                log_string = ('Skipped line #{}: '
                              'product {} already exists.\n').format(
                    reader.line_num,
                    str(product)
                )
                datafile_instance.log += log_string
                datafile_instance.save(update_fields=['log'])
                continue

            product = Product()
            product.url = row['url']
            product.gender = row['gender']

            cats = list()
            cat_fields = ['gender', 'main category',
                          'subcategory', 'subsubcategory']

            for i, name in enumerate(cat_fields):
                parent = None if i == 0 else cats[i-1]
                csv_value = row[name]
                category = Category.objects.get_or_create(
                    name=csv_value, parent=parent)
                cats.append(category)

            product.category = next(i for i in cats[::-1] if i)

            product.brand = Brand.objects.get_or_create(name=row['brand'])
            product.color = Color.objects.get_or_create(name=row['color'])

            product.size = row['size']
            product.material = row['material']

            product.description = row['description']
            product.short_description = row['short description']
            product.meta_description = row['meta description']
            product.title = row['title']
            product.meta_title = row['meta title']

            product.retailer = Retailer.objects.get_or_create(
                name=row['retailer name'])

            product.image_url = row['image url']
            product.free_shipping = bool(row['free shipping'])
            product.available = bool(row['available'])
            product.price = row['price']
            product.sale_price = row['sale price']

            product.save()

            log_string = 'Line #{}: product {} created.\n'.format(
                reader.line_num,
                str(product)
            )
            datafile_instance.log += log_string
            datafile_instance.save(update_fields=['log'])

        if skipped_empty:
            datafile_instance.update_status(
                UploadedFile.ALMOST,
                'Loaded partially, see full log for details.'
            )
        else:
            datafile_instance.update_status(
                UploadedFile.SUCCESS,
                'Successfully loaded.'
            )