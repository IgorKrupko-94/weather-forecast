from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Weather(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания запроса',
        db_index=True)
    user = models.ForeignKey(
        User,
        related_name='weather_requests',
        verbose_name='Пользователь',
        on_delete=models.CASCADE)
    city = models.CharField(max_length=100, verbose_name='Город')
    weather_main = models.CharField(
        max_length=30,
        verbose_name='Группа погодных параметров')
    weather_description = models.CharField(
        max_length=250,
        verbose_name='Состояние погоды в группе')
    temperature = models.FloatField(
        verbose_name='Температура, градусы Цельсия')
    temperature_feels_like = models.FloatField(
        verbose_name='Человеческое восприятие погоды, градусы Цельсия')
    sea_pressure = models.PositiveSmallIntegerField(
        verbose_name='Атмосферное давление на уровне моря, гПа')
    ground_pressure = models.PositiveSmallIntegerField(
        verbose_name='Атмосферное давление на уровне земли, гПа')
    humidity = models.PositiveSmallIntegerField(verbose_name='Влажность, %')
    visibility = models.PositiveSmallIntegerField(
        verbose_name='Видимость, метр')
    wind_speed = models.FloatField(verbose_name='Скорость ветра, метр/сек')
    wind_deg = models.PositiveSmallIntegerField(
        verbose_name='Направление ветра, градусы')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Запрос прогноза погоды'
        verbose_name_plural = 'Запросы прогноза погоды'

    def __str__(self):
        return f'Прогноз погоды за {self.created} в городе {self.city}'
