# core\utils.py
import logging
from telegram import Bot
from django.conf import settings
from asgiref.sync import async_to_sync
from .models import Order, Product
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Order, OrderItem, Report
from django.db.models import Sum, Count, F

logger = logging.getLogger(__name__)

# Проверка и инициализация Telegram бота
def get_bot():
    if settings.ENABLE_TELEGRAM_NOTIFICATIONS and settings.TELEGRAM_BOT_TOKEN:
        return Bot(token=settings.TELEGRAM_BOT_TOKEN)
    else:
        if not settings.ENABLE_TELEGRAM_NOTIFICATIONS:
            logger.warning("Уведомления в Telegram отключены настройками.")
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("Отсутствует TELEGRAM_BOT_TOKEN в настройках.")
        return None

async def async_send_message(chat_id, message):
    bot = get_bot()
    try:
        if bot:
            await bot.send_message(chat_id=chat_id, text=message)
        else:
            logger.warning(f"Сообщение не отправлено. Bot не инициализирован.")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram (chat_id={chat_id}): {e}")

def send_telegram_message(chat_id, message):
    async_to_sync(async_send_message)(chat_id, message)


def generate_sales_report(start_date=None, end_date=None):
    orders = Order.objects.filter(status='delivered')
    reports = Report.objects.filter(created_at__range=(start_date, end_date)).order_by('-created_at')

    if isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            orders = orders.filter(created_at__date__gte=start_date)

        except ValueError:
            logger.error(f"Invalid start_date format: {start_date}")
            start_date = None

    if isinstance(end_date, str):
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            orders = orders.filter(created_at__date__lte=end_date)
        except ValueError:
            logger.error(f"Invalid end_date format: {end_date}")
            end_date = None

    if not orders.exists():
        logger.warning("No orders found for the specified date range.")
    if not reports.exists():
        logger.warning("No reports for CSV-creating found for the specified date range.")

    total_sales = orders.aggregate(total=Sum(F('items__quantity') * F('items__product__price')))['total'] or 0
    total_orders = orders.count()
    total_customers = orders.values('user').distinct().count()

    # # Подготовка данных для графика
    # sales_data = orders.annotate(date_only=F('created_at__date')).values('date_only').annotate(
    #     total=Sum(F('items__quantity') * F('items__product__price'))
    # ).order_by('date_only')

    # Подготовка данных для графика
    sales_data = orders.annotate(date_only=F('created_at__date')).values('date_only').annotate(
        total_sales=Sum(F('items__quantity') * F('items__product__price')),
        orders_per_day=Count('id'),
        unique_customers_per_day=Count('user', distinct=True)
    ).order_by('date_only')

    # csv_data = reports.annotate(date_only=F('created_at__date')).values('date_only').annotate(
    #     total_sales='total_sales',
    #     orders_per_day='total_orders',
    #     unique_customers_per_day='total_customers'
    # ).order_by('date_only')

    csv_data = reports.values('created_at__date', 'total_sales', 'total_orders', 'total_customers').order_by(
        'created_at__date')

    if not sales_data:
        logger.warning("No sales data available for the report.")
    if not csv_data:
        logger.warning("No CSV data available for the report.")

    report = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'sales_data': list(sales_data),
        'csv_data': list(csv_data),
    }

    logger.debug(f"Report Data: {report}")

    return report


# def generate_sales_report(start_date=None, end_date=None):
#     orders = Order.objects.filter(status='delivered')
#
#     if isinstance(start_date, str):
#         try:
#             start_date = datetime.strptime(start_date, '%Y-%m-%d')
#             orders = orders.filter(created_at__date__gte=start_date)
#         except ValueError:
#             logger.error(f"Invalid start_date format: {start_date}")
#             start_date = None  # Игнорируем некорректный формат даты
#
#     if isinstance(end_date, str):
#         try:
#             end_date = datetime.strptime(end_date, '%Y-%m-%d')
#             orders = orders.filter(created_at__date__lte=end_date)
#         except ValueError:
#             logger.error(f"Invalid end_date format: {end_date}")
#             end_date = None  # Игнорируем некорректный формат даты
#
#     total_sales = orders.aggregate(total=Sum(F('items__quantity') * F('items__product__price')))['total'] or 0
#     total_orders = orders.count()
#     total_customers = orders.values('user').distinct().count()
#
#     # Подготовка данных для графика
#     sales_data = orders.annotate(date_only=F('created_at__date')).values('date_only').annotate(
#         total=Sum(F('items__quantity') * F('items__product__price'))
#     ).order_by('date_only')
#
#     report = {
#         'total_sales': total_sales,
#         'total_orders': total_orders,
#         'total_customers': total_customers,
#         'sales_data': list(sales_data),
#     }
#
#     logger.debug(f"Report Data: {report}")  # Отладка
#
#     return report


def generate_sales_report_by_period(start_date=None, end_date=None, days=None):
    # Если указан конкретный период дат, используем его
    if start_date and end_date:
        orders = Order.objects.filter(created_at__range=(start_date, end_date))
    # Иначе используем последние 'days' дней
    elif days:
        end_date = timezone.now()  # Учитываем часовой пояс
        start_date = end_date - timedelta(days=days)
        orders = Order.objects.filter(created_at__range=(start_date, end_date))
    else:
        # Обработка по умолчанию - за последние 30 дней
        end_date = timezone.now()  # Учитываем часовой пояс
        start_date = end_date - timedelta(days=30)
        orders = Order.objects.filter(created_at__range=(start_date, end_date))

    # Исправление: используем метод `get_total_price()`
    total_sales = sum(order.get_total_price() for order in orders)
    total_orders = orders.count()
    total_customers = orders.values('user').distinct().count()

    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_customers': total_customers,
    }


def generate_sales_report_by_custom_period(start_date=None, end_date=None):
    if not start_date or not end_date:
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

    orders = Order.objects.filter(
        created_at__range=[start_date, end_date],
        status='delivered'
    )

    total_sales = orders.aggregate(
        total_sales=Sum(F('items__quantity') * F('items__product__price'))
    )['total_sales'] or 0

    total_orders = orders.count()
    total_customers = orders.values('user').distinct().count()

    report = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_customers': total_customers,
    }

    return report