from django.db import models


class Site(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    main_url = models.CharField(verbose_name='Main url', max_length=50)
    slug = models.SlugField(verbose_name='Slug')

    def __str__(self):
        return self.title
