import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .factories import UserFactory, ProductFactory

@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.fixture
def authenticated_client(client):
    user = UserFactory()
    client.force_login(user)
    return client

@pytest.fixture
def sample_product():
    return ProductFactory()