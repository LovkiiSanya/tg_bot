from django.apps import AppConfig
import os


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def ready(self):
        # Только запускаем бота если это основное приложение и нет миграции или других команд
        # if os.environ.get('RUN_MAIN', None) != 'true' and 'runserver' not in os.environ.get('DJANGO_SETTINGS_MODULE'):
        #     from django.core.management import call_command
        #     try:
        #         call_command('runbot')
        #     except:
        #         print("Error: Command 'runbot' not found or another instance is running")
        pass
