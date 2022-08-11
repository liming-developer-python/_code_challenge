from django.db import models


# Weather data from wx_data
class Weather(models.Model):
    date = models.DateField()
    state = models.IntegerField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    rain_depth = models.FloatField()

    def __str__(self):
        return self.date


# Yield data from yld_data
class Yield(models.Model):
    year = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.year


# Statistics data after get Weather and Yield models
class Statistic(models.Model):
    year = models.IntegerField()
    state = models.IntegerField()
    avg_max_temp = models.FloatField()
    avg_min_temp = models.FloatField()
    total_prec = models.FloatField()
