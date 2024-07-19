from django.urls import path

from .views import GetWeatherAPIView


urlpatterns = [
    path('get_weather_forecast', GetWeatherAPIView.as_view()),
]
