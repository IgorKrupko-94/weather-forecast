from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CitySerializer, WeatherSerializer
from .services import ParseWeather


class GetWeatherAPIView(APIView):
    def post(self, request):
        user = self.request.user
        serializer = CitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        weather_request = ParseWeather(user, serializer.validated_data['city'])
        try:
            result_weather = weather_request.run()
        except Exception:
            return Response(
                data={'message': 'При попытке получения прогноза погоды'
                                 ' произошла ошибка. Пожалуйста,'
                                 ' попробуйте позже.'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            weather_serializer = WeatherSerializer(result_weather)
            return Response(weather_serializer.data, status=status.HTTP_200_OK)
