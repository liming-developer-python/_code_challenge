from django.db import models


# Create your models here.
class Weather(models.Model):
    date = models.DateField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    rain_depth = models.FloatField()

    def __str__(self):
        return self.date


class Yield(models.Model):
    year = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.year

