from django.db import models


class Site(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    main_url = models.CharField(verbose_name='Main url', max_length=50)
    slug = models.CharField(verbose_name='Pseudo slug', max_length=100)
    name_for_crauler = models.SlugField(max_length=40,
                                        verbose_name='Main slug', null=True)

    def __str__(self):
        return self.title
