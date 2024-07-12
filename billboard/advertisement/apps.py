from django.apps import AppConfig


import redis


class AdvertisementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advertisement'

    def ready(self):
            from advertisement import signals  # выполнение модуля -> регистрация сигналов


r = redis.Redis(
  host='redishost',
  port='port',
  password='password')


