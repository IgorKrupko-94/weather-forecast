from rest_framework import serializers

from .models import Weather


class CitySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'
