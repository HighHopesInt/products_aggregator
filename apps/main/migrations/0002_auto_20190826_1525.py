# Generated by Django 2.0.12 on 2019-08-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='meta_title',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]