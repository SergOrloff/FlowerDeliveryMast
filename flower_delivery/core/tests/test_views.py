from django.test import TestCase, Client
from django.urls import reverse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.models import Product, CartItem
from .factories import ProductFactory, UserFactory

class ProductViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.product = ProductFactory(stock=10)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_add_to_cart_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {'quantity': 2})
        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(CartItem.objects.count(), 1)

    def test_checkout_process(self):
        self.client.force_login(self.user)
        self.client.post(reverse('add_to_cart', args=[self.product.id]), {'quantity': 2})
        response = self.client.post(reverse('checkout'), {
            'address': 'ул. Цветочная, 15',
            'payment_method': 'online'
        })
        self.assertRedirects(response, reverse('order_success'))
        self.assertEqual(self.product.stock, 8)

class AuthTests(TestCase):
    def test_login_redirect(self):
        response = self.client.get(reverse('cart'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("cart")}')