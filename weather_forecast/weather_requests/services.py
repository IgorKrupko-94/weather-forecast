import json
import os

import httpx

from .models import Weather


class ParseWeather:
    URL_GEO = 'http://api.openweathermap.org/geo/1.0/direct'
    URL_WEATHER = 'https://api.openweathermap.org/data/2.5/weather'
    APP_ID = os.getenv('API_WEATHER_KEY')
    LIMIT = 1
    coord = {}
    result_weather = {}

    def __init__(self, user, city):
        self.user = user
        self.city = city

    def get_coordinates(self):
        query_params = {'q': self.city, 'limit': self.LIMIT,
                        'appid': self.APP_ID}
        try:
            response = httpx.get(self.URL_GEO, params=query_params, timeout=2)
        except Exception:
            raise RuntimeError
        else:
            if response.status_code != 200:
                raise RuntimeError
            response = json.loads(response.text)
            if not response:
                raise RuntimeError
            self.coord['lat'] = response[0]['lat']
            self.coord['lon'] = response[0]['lon']

    def get_weather(self):
        query_params = {'lat': self.coord['lat'],
                        'lon': self.coord['lon'],
                        'appid': self.APP_ID,
                        'units': 'metric'}
        try:
            response = httpx.get(self.URL_WEATHER, params=query_params,
                                 timeout=2)
        except Exception:
            raise RuntimeError
        else:
            if response.status_code != 200:
                raise RuntimeError
            response = json.loads(response.text)
            if not response:
                raise RuntimeError
            self.result_weather = {
                'user': self.user,
                'city': self.city,
                'weather_main': response['weather'][0]['main'],
                'weather_description': response['weather'][0]['description'],
                'temperature': response['main']['temp'],
                'temperature_feels_like': response['main']['feels_like'],
                'sea_pressure': response['main']['sea_level'],
                'ground_pressure': response['main']['grnd_level'],
                'humidity': response['main']['humidity'],
                'visibility': response['visibility'],
                'wind_speed': response['wind']['speed'],
                'wind_deg': response['wind']['deg']
            }

    def upload_db(self):
        obj = Weather.objects.create(**self.result_weather)
        return obj

    def run(self):
        try:
            self.get_coordinates()
            self.get_weather()
            obj = self.upload_db()
        except Exception:
            raise RuntimeError
        else:
            return obj
