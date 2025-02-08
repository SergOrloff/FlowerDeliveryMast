# flower_delivery\flower_delivery\asgi.py
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')

application = get_asgi_application()
