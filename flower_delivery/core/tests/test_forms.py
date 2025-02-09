from django.test import TestCase
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.forms import LoginForm, ProductForm
from .factories import UserFactory, ProductFactory

class LoginFormTests(TestCase):
    def test_valid_login(self):
        user = UserFactory(password='testpass123')
        form = LoginForm(data={
            'username': user.username,
            'password': 'testpass123'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_login(self):
        form = LoginForm(data={
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertFalse(form.is_valid())

class ProductFormTests(TestCase):
    def test_product_validation(self):
        form = ProductForm(data={
            'name': 'Test Product',
            'price': -100,
            'stock': 10
        })
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)