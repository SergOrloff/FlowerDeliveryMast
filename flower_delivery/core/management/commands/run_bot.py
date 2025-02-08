# core/management/commands/run_bot.py
import logging
import os
import sys
from django.core.management.base import BaseCommand
# Добавляем путь к корневой папке проекта, чтобы Python мог найти модуль telegram_bot
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
# print(sys.path)
from telegram_bot import setup_bot

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Запуск Telegram бота...'))
        try:
            setup_bot()
            self.stdout.write(self.style.SUCCESS('Telegram бот успешно остановлен.'))
        except Exception as e:
            logger.error(f"Ошибка при запуске Telegram бота: {e}")
            self.stdout.write(self.style.ERROR(f'Ошибка при запуске Telegram бота: {e}'))
