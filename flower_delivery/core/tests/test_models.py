from django.test import TestCase
from .factories import (
    ProductFactory,
    UserFactory,
    OrderFactory,
    ReportFactory
)
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.models import Product, Order, UserProfile, Report

class ProductModelTests(TestCase):
    def test_product_availability(self):
        product = ProductFactory(stock=5)
        self.assertTrue(product.is_available)

        product.stock = 0
        self.assertFalse(product.is_available)

    def test_stock_management(self):
        product = ProductFactory(stock=10)
        product.decrease_stock(3)
        self.assertEqual(product.stock, 7)

        with self.assertRaises(ValueError):
            product.decrease_stock(20)


class OrderModelTests(TestCase):
    def test_order_creation(self):
        user = UserFactory()
        order = OrderFactory(user=user, total=1500.00)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.user.orders.count(), 1)


class ReportModelTests(TestCase):
    def test_report_generation(self):
        report = ReportFactory()
        self.assertIsNotNone(report.created_at)
        self.assertGreater(report.total_sales, 0)