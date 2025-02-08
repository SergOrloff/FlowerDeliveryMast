# core/tests.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.test import TestCase
from django.urls import reverse
from .models import Product, Order, OrderItem
from django.test import Client
from django.contrib.auth.models import User

class OrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        cls.client = Client()
        # Добавляем created_by при создании продукта
        cls.product = Product.objects.create(
            name="Тестовый продукт",
            price=10,
            created_by=cls.user  # Добавленная строка
        )

    def test_create_order(self):
        order = Order.objects.create(user=self.user, address="Тестовый адрес")
        OrderItem.objects.create(order=order, product=self.product, quantity=2)

        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.get_total_price(), 20)
        self.assertEqual(order.address, "Тестовый адрес")
        self.assertEqual(order.status, "pending")  # Предполагаемый статус по умолчанию
        self.assertEqual(order.user, self.user)

    def test_repeat_order(self):
        order = Order.objects.create(user=self.user, address="Тестовый адрес")
        OrderItem.objects.create(order=order, product=self.product, quantity=1)

        # Аутентифицируем клиента
        self.client.login(username='testuser', password='testpassword')

        # Используем reverse для получения URL
        response = self.client.get(reverse('repeat_order', args=[order.id]))
        self.assertEqual(response.status_code, 302)

        new_order = Order.objects.last()
        self.assertNotEqual(order.id, new_order.id)  # Проверка, что новый заказ создан
        self.assertEqual(new_order.items.count(), 1)
        self.assertEqual(new_order.get_total_price(), 10)
        self.assertEqual(new_order.user, self.user)
        self.assertEqual(new_order.address, order.address)

        # Проверяем перенаправление
        self.assertRedirects(response, reverse('order_detail', args=[new_order.id]))

    def test_repeat_order_unauthenticated(self):
        order = Order.objects.create(user=self.user, address="Тестовый адрес")
        OrderItem.objects.create(order=order, product=self.product, quantity=1)

        response = self.client.get(reverse('repeat_order', args=[order.id]))
        # self.assertNotEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа
        self.assertIn('/login/', response.url)

    def test_repeat_other_users_order(self):
        other_user = User.objects.create_user(username="otheruser", password="otherpassword")
        order = Order.objects.create(user=other_user, address="Другой адрес")
        OrderItem.objects.create(order=order, product=self.product, quantity=1)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('repeat_order', args=[order.id]))
        self.assertEqual(response.status_code, 403)  # Ожидаем отказ в доступе

    def test_repeat_nonexistent_order(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('repeat_order', args=[9999]))
        self.assertEqual(response.status_code, 404)

class ReportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')

    def test_sales_report_access(self):
        # Пытаемся получить доступ без авторизации
        response = self.client.get('/reports/sales/')
        self.assertEqual(response.status_code, 302)  # Должен перенаправить на страницу входа

        # Авторизуемся как администратор
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/reports/sales/')
        self.assertEqual(response.status_code, 200)

class ReportsTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.client = Client()
        self.client.login(username='admin', password='adminpassword')

        # Создаем тестовые данные
        product = Product.objects.create(
            name='Тестовый продукт',
            price=100,
            created_by=self.admin_user  # Добавляем создателя
        )
        order = Order.objects.create(user=self.admin_user, status='delivered')
        OrderItem.objects.create(order=order, product=product, quantity=2)

    def test_sales_report_view(self):
        response = self.client.get(reverse('sales_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Общий объем продаж')

    def test_popular_products_report_view(self):
        response = self.client.get(reverse('popular_products_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый продукт')
