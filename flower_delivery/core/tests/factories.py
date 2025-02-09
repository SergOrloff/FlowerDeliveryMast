import factory
import random
from django.contrib.auth import get_user_model
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.models import Product, Order, CartItem, Report

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=0, max=100)
    description = factory.Faker('text')

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    status = 'pending'

class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Report

    total_sales = factory.Faker('random_int', min=1000, max=100000)
    total_orders = factory.Faker('random_int', min=1, max=100)
    total_customers = factory.Faker('random_int', min=1, max=50)