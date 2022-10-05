from django.db import models


class City(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60, blank=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        ordering = ['name']