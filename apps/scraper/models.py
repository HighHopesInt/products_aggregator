from django.db import models


class Site(models.Model):
    title = models.CharField(verbose_name='Title', max_length=50)
    url = models.CharField(verbose_name='Url', max_length=150)
    name_for_crauler = models.CharField(verbose_name='Main slug',
                                        max_length=40,
                                        null=True)

    def __str__(self):
        return self.title
