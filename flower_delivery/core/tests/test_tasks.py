from unittest.mock import patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.tasks import generate_daily_report, send_order_notification

def test_generate_daily_report(mocker):
    mock_send = mocker.patch('core.tasks.send_report_email')
    generate_daily_report.delay()
    mock_send.assert_called_once()

def test_order_notification(mocker):
    mock_bot = mocker.patch('core.tasks.telegram_bot.send_message')
    send_order_notification.delay(123, 1500.00)
    mock_bot.assert_called_once_with(123, "Новый заказ на сумму 1500.00 руб.")
