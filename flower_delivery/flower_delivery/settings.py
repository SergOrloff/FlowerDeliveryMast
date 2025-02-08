# flower_delivery\flower_delivery\settings.py
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import environ
import os
import sys
if sys.platform.startswith('win'):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from .settings import *

BASE_DIR = Path(__file__).resolve().parent.parent
os.environ['KALEIDO_TMP'] = os.path.join(BASE_DIR, 'tmp')
os.makedirs(os.environ['KALEIDO_TMP'], exist_ok=True)
PLOTLY_IO_KALEIDO_SCOPE = {
    'timeout': 60,
    'mathjax': False
}


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-aj49+pk6yxa75+a2+nnmh3dwt61ycss^-655+v3z39&3dvmxu1')

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
DOMAIN_NAME = 'http://127.0.0.1:8000'  # Используйте IP-адрес и порт вашего локального сервера

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'widget_tweaks',
    'dadata',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'flower_delivery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flower_delivery.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
PLOTLY_IO_KALEIDO_SCOPE = {
    'timeout': 60,
    'mathjax': False,
    'quiet': True,
    'scale': 2
}
PLOTLY_IO_IMAGE_FORMAT = 'png'
PLOTLY_IO_IMAGE_ENGINE = 'kaleido'
CHOREOGRAPHER_DEBUG_BROWSER = True  # Для диагностики
CHOREOGRAPHER_BROWSER_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'  # Явное указание браузера
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# Инициализация переменных окружения
env = environ.Env()
environ.Env.read_env('.env')
env.read_env(env_file='.env.test')

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", default="your_bot_token_here")
ADMIN_TELEGRAM_CHAT_ID = env("ADMIN_TELEGRAM_CHAT_ID", default="your_admin_chat_id_here")
ENABLE_TELEGRAM_NOTIFICATIONS = env.bool("ENABLE_TELEGRAM_NOTIFICATIONS", default=True)

# SMTP настройки
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.example.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='your_default_email@example.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='test@example.com')
ADMIN_EMAIL = env('ADMIN_EMAIL', default='test@example.com')
ENABLE_EMAIL_NOTIFICATIONS = env.bool("ENABLE_EMAIL_NOTIFICATIONS", default=True)


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

COOKIE_CONSENT_NAME = 'cookiesAccepted'
COOKIE_CONSENT_AGE_DAYS = 365

DADATA_API_KEY = env('DADATA_API_KEY', default='')
DADATA_SECRET_KEY = env('DADATA_SECRET_KEY', default='')

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # Две недели

# Настройки рабочее время
WORKING_HOURS_START = 7  # Начало рабочего дня (9 утра)
WORKING_HOURS_END = 20   # Конец рабочего дня (6 вечера)
WORKING_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Понедельник - Суббота (0 - Понедельник, 5 - Суббота)

# SECURE_HSTS_SECONDS = 31536000  # Включите строгий транспортный уровень безопасности
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True  # Перенаправление на HTTPS

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
RECAPTCHA_SECRET_KEY = '6Lcmv7QqAAAAADl6VRJCk5EiTdxCBaH7Z-4K9IBX'
YOUR_RECAPTCHA_SITE_KEY = '6Lcmv7QqAAAAAJ1PBvEJAK8ztRUbMSa8TLf6Obty'
