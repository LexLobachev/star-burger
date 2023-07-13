from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=200, unique=True, verbose_name='Адрес')
    datetime = models.DateTimeField(auto_now=True, verbose_name='Дата')
    lat = models.FloatField(null=True, blank=True, verbose_name='Широта')
    lon = models.FloatField(null=True, blank=True, verbose_name='Долгота')

    def __str__(self):
        return f'{self.address}'
