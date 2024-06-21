
from django.apps import AppConfig
from django.conf import settings
import threading


class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        from .bot import main
        if settings.DEBUG:
            threading.Thread(target=main).start()
