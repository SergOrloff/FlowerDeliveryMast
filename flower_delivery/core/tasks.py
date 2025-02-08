from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .utils import generate_sales_report_by_period

@shared_task
def send_daily_sales_report():
    today = timezone.now().date()
    report = generate_sales_report_by_period(1)
    send_mail(
        f'Ежедневный отчет по продажам {today}',
        f'Общий объем продаж: {report["total_sales"]}\n'
        f'Общее количество заказов: {report["total_orders"]}\n'
        f'Общее количество клиентов: {report["total_customers"]}',
        '6202818@gmail.com',
        ['6202818@gmail.com']
    )
