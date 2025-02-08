# core\apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        try:
            import core.signals
        except ImportError as e:
            # Логирование ошибки или другое действие
            print(f"Ошибка импорта сигналов: {e}")