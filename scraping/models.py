from django.db import models
from .utils import from_cyrillic_to_eng
# import jsonfield


def default_urls():
    return {
        'habr': '',
        'hh': '',
    }


class City(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name of the city', unique=True)
    slug = models.CharField(max_length=60, blank=True, unique=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=60, verbose_name='Programming language', unique=True)
    slug = models.CharField(max_length=60, blank=True, unique=True)

    class Meta:
        verbose_name = 'programming language'
        verbose_name_plural = 'programming languages'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Job title')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Job description')
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             verbose_name='City')
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name='Programming language')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'vacancy'
        verbose_name_plural = 'vacancy'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)
        # The function should return a string value


class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             verbose_name='City')
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name='Programming language')
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
    #
    # def __str__(self):
    #     return self.language, self.city

