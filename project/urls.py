from django.urls import path

from . import views

urlpatterns = [
    path('weather', views.api_weather, name='weather'),
    path('yield', views.api_yield, name='yield'),
    path('weather/stats', views.api_weather_stat, name='weather_stat'),
    path('update', views.update_data, name='update_database')
]