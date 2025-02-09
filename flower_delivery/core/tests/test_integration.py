from django.test import TestCase
from django.urls import reverse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.models import Order, CartItem
from .factories import UserFactory, ProductFactory

class FullOrderFlowTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(stock=5)
        self.client.force_login(self.user)

    def test_complete_order_flow(self):
        # Добавление в корзину
        self.client.post(reverse('add_to_cart', args=[self.product.id]), {'quantity': 2})

        # Проверка корзины
        cart_response = self.client.get(reverse('cart'))
        self.assertContains(cart_response, self.product.name)

        # Оформление заказа
        order_response = self.client.post(reverse('checkout'), {
            'address': 'ул. Тестовая, 1',
            'payment_method': 'cash'
        })
        self.assertRedirects(order_response, reverse('order_success'))

        # Проверка обновления запасов
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # Проверка создания заказа
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total, self.product.price * 2)