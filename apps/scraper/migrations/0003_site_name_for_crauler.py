# Generated by Django 2.0.12 on 2019-08-26 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20190813_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='name_for_crauler',
            field=models.SlugField(max_length=10, null=True, verbose_name='Main slug'),
        ),
    ]
