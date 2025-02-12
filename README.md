# FlowerDeliveryMast — профессиональное решение для управления флористическим бизнесом: онлайн-продажи, складской учёт, аналитика и автоматизация.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-brightgreen.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Flower Delivery shop — система управления доставкой цветов в виде реализованного на Django приложения, интегрированного с чат-ботом на базе Телеграм - . Проект предоставляет функционал интернет-магазина с возможностью управления товарами, корзиной, заказами, отзывами и аналитикой.

### 📖Описание
- Приложение позволяет пользователям просматривать каталог цветов и букетов, добавлять товары в корзину, оформлять заказы и оставлять отзывы о продуктах. Администраторы и менеджеры могут управлять товарами, отслеживать заказы и просматривать отчеты по продажам.

### ⚙️ Функциональные возможности
- Каталог товаров: просмотр товаров по категориям, детальная информация о каждом продукте, интеллектуальный поиск и фильтрация.
- Корзина: многоэтапное оформление заказа, добавление товаров в корзину, изменение количества, удаление товаров.
- Оформление заказа: ввод адреса доставки, комментариев, подтверждение заказа.
- История заказов: просмотр предыдущих заказов, повторное оформление заказа, статус-трекинг.
- Отзывы: оставление отзывов и рейтингов для продуктов.
- Управление товарами: добавление, редактирование и удаление товаров (для менеджеров).
- Отчеты по продажам: генерация отчетов с графиками и визуализация данных (графики и диаграммы)в приложении, экспорт в CSV и PDF (для администраторов все отчеты, для пользователей -  отчет по популярным продуктам).
- Интеграция с Telegram администратора и персонала интернет-магазина: уведомления о новых заказах через Telegram-бота, доступ ко всей функциональности приложения и админпанели.
- Поиск адресов: автодополнение адресов с использованием API DaData.
- Реализация GDPR (General Data Protection Regulation): экспорт данных пользователя и удаление аккаунта по запросу.
- Информирование пользователя интернет-магазина о политике конфиденциальности

## 🛠 Технологический стек

- **Бэкенд**: Django 4.2, Django REST Framework
- **База данных**: SQLite (+ Redis для кеширования)
- **Асинхронные задачи**: Celery + Redis
- **Графики**: Plotly
- **Тестирование**: pytest, Factory Boy, Coverage
- **Деплой**: Docker, Nginx, Gunicorn

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- SQLite 3+
- Redis 6+
- Virtualenv

### 🛠️ Установка и запуск

1. Клонируйте репозиторий:

````
git clone https://github.com/SergOrloff/FlowerDeliveryMast.git
cd flower_delivery
````
2. Создайте и активируйте виртуальное окружение:

````
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
````
3. Установите зависимости:

````
pip install -r requirements.txt
````
4. Выполните миграции базы данных:

````
python manage.py migrate
````
5. Создайте суперпользователя:

````
python manage.py createsuperuser
````
6. Соберите статику:

````
python manage.py collectstatic
````
7. Запустите сервер разработки:

````
python manage.py runserver
````
8. Приложение будет доступно по адресу http://127.0.0.1:8000/.

### 📚 Использование приложения
#### Для пользователей
- Регистрация и авторизация: зарегистрируйтесь на сайте или войдите в свой аккаунт.
- Просмотр каталога: перейдите на страницу каталога и выберите интересующие товары. При необходимости отфильтруйте по одной из 8 категорий товара (`Розы`, `Тюльпаны`, `Орхидеи`, `Лилии`, `Пионы`, `Ромашки`, `Букеты`, `Другие`)
- Добавление в корзину: добавьте товары в корзину, укажите количество.
- Оформление заказа: перейдите в корзину и нажмите "Оформить заказ", заполните необходимые данные (при этом оформить заказ можно только в рабочее время для персонала время - с 10 до 18 часов).
- История заказов: в личном кабинете (ЛК) вы можете просматривать свои заказы и повторять их. Также для пользователей в ЛК доступен отчет о популярных продуктах
- Оставление отзывов: на странице продукта вы можете оставить отзыв и рейтинг.
#### Для менеджеров и администраторов
- Доступ в админ-панель: перейдите по адресу http://127.0.0.1:8000/admin/ и войдите под учетной записью администратора.
- Управление товарами: добавляйте новые продукты, редактируйте существующие, управляйте остатками на складе.
- Управление заказами: просматривайте новые заказы, обновляйте их статус, связывайтесь с клиентами при необходимости.
- Просмотр отчетов: в разделе отчетов вы можете генерировать отчеты по продажам за различные периоды, экспортировать их в CSV или PDF.

### 📚 Использование телеграм-бота FlowerDeliveryBot (с именем @Flow_Deliv_Bot)
#### Для пользователей
- Регистрация и авторизация: зарегистрируйтесь в боте (для тех, кто впервые заказывает цветы. Обязательное условие - в личном аккаунте должно быть заведено имя пользователя).
- Просмотр каталога (идет маршрутизация на страницу каталога приложения и выберите интересующие товары). Если необходимо заказать товар по одной  позиции, в боте имеется такая возможность.
- Оформление заказа: укажите количество товара и нажмите "Подтвердить заказ".

#### Для менеджеров и администраторов
- Отслеживание информации о поступивших заказах.
- Доступ в админ-панель из бота: перейдите по адресу http://127.0.0.1:8000/admin/ и войдите под учетной записью администратора.

## 📚 Документация разработчика
### 🔧 Настройки

- Для работы некоторых функций приложения необходимо создать файл .env в корневой директории и указать в нем следующие переменные:

````
# Django Secret Key
DJANGO_SECRET_KEY='ваш ключ'

# Включить режим отладки (True/False)
DJANGO_DEBUG=True

# Настройки SMTP для отправки писем
EMAIL_HOST_USER='exempl@exempl.ru'
EMAIL_HOST_PASSWORD='@123456789'
DEFAULT_FROM_EMAIL='exempl@exempl.ru''
ADMIN_EMAIL='exempl@exempl.ru''
ENABLE_EMAIL_NOTIFICATIONS=true  # или false, чтобы отключить почтовые уведомления
EMAIL_HOST='smtp.yandex.ru' #Можно использовать любой
EMAIL_PORT= 587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false

# Ключи для DaData API
DADATA_API_KEY='ваш ключ'
DADATA_SECRET_KEY='ваш ключ'

TELEGRAM_BOT_TOKEN='ваш токен'
ADMIN_TELEGRAM_CHAT_ID=ваш ID
ENABLE_TELEGRAM_NOTIFICATIONS=true  # или false, чтобы отключить уведомления
````

#### 📊 Инициализация данных
Для загрузки демо-данных выполните:
````bash
python manage.py loaddata core/fixtures/initial_data.json
````
Команда создаст:
- 22 тестовых товара;
- 8 категорий товара;
- 5 демо-пользователей;
- примеры заказов и отзывов.

#### Настройка Telegram бота
1. Создайте бота с помощью @BotFather в Telegram и получите токен.
2. Укажите токен в переменной TELEGRAM_BOT_TOKEN в файле .env.
3. В модели UserProfile предусмотрено поле telegram_chat_id. Пользователи могут связать свой аккаунт с Telegram для получения уведомлений.

#### Настройка DaData
1. Зарегистрируйтесь на DaData.ru и получите API-токен.
2. Укажите токен в переменной DADATA_API_TOKEN в файле .env.

### 📊 Отчеты и аналитика
#### Отчеты по продажам доступны в админ-панели, а также в личном кабинете пользователя (админу и персоналу доступны четыре отчета с выводом информации о динамике продаж в форматах CSV и PDF, а рядовому пользователю - отчет о популярных продуктах интернет-магазина).
- Вы можете выбирать период отчета, просматривать графики продаж, экспорта данных в CSV и PDF.
- Для генерации графиков используется библиотека Plotly.
- PDF-отчеты формируются с помощью ReportLab.

### 🛡️ Безопасность и GDPR
- Реализована возможность экспорта данных пользователя в соответствии с требованиями GDPR.
- Пользователи могут запросить удаление своего аккаунта и данных.

#### 📦 Зависимости
##### Основные библиотеки и фреймворки, используемые в проекте:
````
Django
Django Widgets
Python Telegram Bot
Requests
ReportLab
Plotly
Pandas
DaData API
````
Полный список зависимостей указан в файле requirements.txt.

### 🧪 Тестирование
#### Запуск всех тестов с покрытием:
```
bash
pytest --cov=core --cov-report=html
```
Откройте htmlcov/index.html для просмотра отчёта о покрытии.

### 🖥 Основные команды управления
#### Запуск Celery worker:
````
bash
celery -A flower_delivery worker -l info
````

#### Генерация ежедневного отчёта:
````
bash
python manage.py generate_reports
````
#### Запуск Telegram-бота:
````
bash
python manage.py run_bot
````

#### 📈 Производительность
Для оптимизации в продакшн-режиме:
````
bash
# Сбор статики
python manage.py collectstatic --noinput

# Кеширование шаблонов
python manage.py compress

# Запуск в production-режиме
gunicorn --workers 4 --bind 0.0.0.0:8000 flower_delivery.wsgi:application
````
### Структура проекта
````
├── .env
├── .pytest_cache/
│   ├── CACHEDIR.TAG
│   ├── README.md
│   ├── v/
│   │   ├── cache/
│   │   │   ├── lastfailed
│   │   │   ├── nodeids
│   │   │   ├── stepwise
├── bot/
│   ├── __init__.py
├── bot_logs.log
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── fixtures/
│   ├── fonts/
│   │   ├── DejaVuSans-Bold.ttf
│   │   ├── DejaVuSans-BoldOblique.ttf
│   │   ├── DejaVuSans-ExtraLight.ttf
│   │   ├── DejaVuSans-Oblique.ttf
│   │   ├── DejaVuSans.ttf
│   │   ├── Roboto-Italic.ttf
│   │   ├── Roboto.ttf
│   ├── forms.py
│   ├── management/
│   │   ├── commands/
│   │   │   ├── generate_reports.py
│   │   │   ├── run_bot.py
│   ├── migrations/
│   │   ├── __init__.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks.py
│   ├── templatetags/
│   │   ├── core_tags.py
│   │   ├── form_filters.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── factories.py
│   │   ├── test_forms.py
│   │   ├── test_integration.py
│   │   ├── test_models.py
│   │   ├── test_tasks.py
│   │   ├── test_views.py
│   │   ├── __init__.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   ├── __init__.py
├── db.sqlite3
├── flower_delivery/
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── __init__.py
├── manage.py
├── media/
│   ├── products/
│   │   ├── 110-sm-mishka-haki-01-405x405.webp
│   │   ├── 15-kustovyh-romashek-v-korzine-04-900x900.webp
│   │   ├── 15-roz-silva-pink-40-sm-405x405.webp
│   │   ├── 15-sirenevyh-roz-60-sm-405x405.webp
│   │   ├── 17-sinih-orhidey-dendrobium-v-korzine-405x405.webp
│   │   ├── 25-liliy-miks-900x900.webp
│   │   ├── 25-liliy-miks-900x900_rxoiRzt.webp
│   │   ├── 25-pionov-sara-bernar-v-korobke-900x900.webp
│   │   ├── 25-tyulpanov-kolumbus-0-900x900.webp
│   │   ├── 25-tyulpanov-miks-99-405x405.webp
│   │   ├── 35-krasnyh-roz-70-sm-900x900.webp
│   │   ├── 35-tyulpanov-krasnyh-99-405x405.webp
│   │   ├── 5-belo-rozovyh-orhidey-897x900.webp
│   │   ├── 501-krasnaya-roza-40-sm-990-900x900.webp
│   │   ├── 51-krasnyy-pion-v-upak-9-900x900.webp
│   │   ├── 75-kustovyh-romashek-04-899x899.webp
│   │   ├── 9-rozovyh-liliy-900x900.webp
│   │   ├── bel-pion-i-roz-gorten-v-korobke-900x900.webp
│   │   ├── buket-dnya-suhocvety--roza-i-bulgur-v-yashchike-405x405.webp
│   │   ├── buket-nevesty-kremovaya-gipsofila-900x900.webp
│   │   ├── buket-nevesty-siniy-dendrobium-405x405.webp
│   │   ├── buket-rozarium2-405x405.webp
│   │   ├── desktop.ini
│   │   ├── konfety-zoloto-v-korobke-405x405.webp
│   │   ├── mandarin-korica-900x854.webp
│   ├── temp/
├── pytest.ini
├── requirements.txt
├── seckey_djng.py
├── static/
│   ├── css/
│   │   ├── styles.css
│   ├── images/
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   ├── logo__.png
│   │   ├── promo1.jpg
│   │   ├── promo2.jpg
│   │   ├── promo3.jpg
│   │   ├── promo4.jpg
│   │   ├── rutube.png
│   │   ├── success-icon — копия.png
│   │   ├── success-icon.png
│   │   ├── success-icon1.png
│   │   ├── telegram.png
│   │   ├── tulpan/
│   │   │   ├── flower-empty.png
│   │   │   ├── flower-empty1.png
│   │   │   ├── flower-filled.png
│   │   │   ├── flower-filled1.png
│   │   │   ├── tulip_flower_icon_cb.svg
│   │   │   ├── tulip_flower_icon_contr.svg
│   │   │   ├── tulip_flower_spring_icon_219602.svg
│   │   ├── vk.png
├── staticfiles/
│   ├── admin/
│   │   ├── css/
│   │   │   ├── autocomplete.css
│   │   │   ├── base.css
│   │   │   ├── changelists.css
│   │   │   ├── dark_mode.css
│   │   │   ├── dashboard.css
│   │   │   ├── forms.css
│   │   │   ├── login.css
│   │   │   ├── nav_sidebar.css
│   │   │   ├── responsive.css
│   │   │   ├── responsive_rtl.css
│   │   │   ├── rtl.css
│   │   │   ├── unusable_password_field.css
│   │   │   ├── vendor/
│   │   │   │   ├── select2/
│   │   │   ├── widgets.css
│   │   ├── img/
│   │   │   ├── address-card-regular.svg
│   │   │   ├── calendar-icons.svg
│   │   │   ├── favicon.ico
│   │   │   ├── gis/
│   │   │   │   ├── move_vertex_off.svg
│   │   │   │   ├── move_vertex_on.svg
│   │   │   ├── icon-addlink.svg
│   │   │   ├── icon-alert.svg
│   │   │   ├── icon-calendar.svg
│   │   │   ├── icon-changelink.svg
│   │   │   ├── icon-clock.svg
│   │   │   ├── icon-deletelink.svg
│   │   │   ├── icon-hidelink.svg
│   │   │   ├── icon-no.svg
│   │   │   ├── icon-unknown-alt.svg
│   │   │   ├── icon-unknown.svg
│   │   │   ├── icon-viewlink.svg
│   │   │   ├── icon-yes.svg
│   │   │   ├── inline-delete.svg
│   │   │   ├── LICENSE
│   │   │   ├── README.txt
│   │   │   ├── search.svg
│   │   │   ├── selector-icons.svg
│   │   │   ├── sorting-icons.svg
│   │   │   ├── tooltag-add.svg
│   │   │   ├── tooltag-arrowright.svg
│   │   ├── js/
│   │   │   ├── actions.js
│   │   │   ├── admin/
│   │   │   │   ├── DateTimeShortcuts.js
│   │   │   │   ├── RelatedObjectLookups.js
│   │   │   ├── autocomplete.js
│   │   │   ├── calendar.js
│   │   │   ├── cancel.js
│   │   │   ├── change_form.js
│   │   │   ├── core.js
│   │   │   ├── filters.js
│   │   │   ├── inlines.js
│   │   │   ├── jquery.init.js
│   │   │   ├── nav_sidebar.js
│   │   │   ├── popup_response.js
│   │   │   ├── prepopulate.js
│   │   │   ├── prepopulate_init.js
│   │   │   ├── SelectBox.js
│   │   │   ├── SelectFilter2.js
│   │   │   ├── theme.js
│   │   │   ├── unusable_password_field.js
│   │   │   ├── urlify.js
│   │   │   ├── vendor/
│   │   │   │   ├── jquery/
│   │   │   │   ├── select2/
│   │   │   │   ├── xregexp/
│   ├── css/
│   │   ├── styles.css
│   ├── images/
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   ├── logo__.png
│   │   ├── promo1.jpg
│   │   ├── promo2.jpg
│   │   ├── promo3.jpg
│   │   ├── promo4.jpg
│   │   ├── rutube.png
│   │   ├── success-icon — копия.png
│   │   ├── success-icon.png
│   │   ├── success-icon1.png
│   │   ├── telegram.png
│   │   ├── tulpan/
│   │   │   ├── flower-empty.png
│   │   │   ├── flower-empty1.png
│   │   │   ├── flower-filled.png
│   │   │   ├── flower-filled1.png
│   │   │   ├── tulip_flower_icon_cb.svg
│   │   │   ├── tulip_flower_icon_contr.svg
│   │   │   ├── tulip_flower_spring_icon_219602.svg
│   │   ├── twitter.png
│   │   ├── vk.png
├── telegram_bot.py
├── templates/
│   ├── about.html
│   ├── add_product.html
│   ├── add_review.html
│   ├── admin/
│   │   ├── popular_products_report_adm.html
│   │   ├── reports_list_adm.html
│   │   ├── sales_report.html
│   │   ├── sales_report_site_adm.html
│   │   ├── sales_report_site_adm0.html
│   ├── base.html
│   ├── cart.html
│   ├── catalog.html
│   ├── checkout.html
│   ├── confirm_delete.html
│   ├── contact.html
│   ├── delete_user.html
│   ├── edit_product.html
│   ├── edit_user.html
│   ├── order_detail.html
│   ├── order_history.html
│   ├── order_success.html
│   ├── pagination.html
│   ├── privacy_policy.html
│   ├── product_detail.html
│   ├── profile.html
│   ├── registration/
│   │   ├── login.html
│   │   ├── password_reset.html
│   │   ├── register.html
│   ├── reports/
│   │   ├── popular_products_report.html
│   │   ├── reports_list.html
│   │   ├── sales_report_site.html
│   │   ├── sales_report_site_fig.html
│   ├── update_stock.html
│   ├── user_list.html
├── __init__.py
````

### Интеграция с Telegram
````
python
# Отправка уведомления администратору о создании нового заказа
@receiver(post_save, sender=Order)
def notify_admin_order_created(sender, instance, created, **kwargs):
    if created and settings.ADMIN_TELEGRAM_CHAT_ID:
        message = f"Новый заказ создан: #{instance.id} пользователем {instance.user.username}."
        try:
            send_telegram_message(settings.ADMIN_TELEGRAM_CHAT_ID, message)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления администратору: {e}")
    elif not settings.ADMIN_TELEGRAM_CHAT_ID:
        logger.warning("ADMIN_TELEGRAM_CHAT_ID не задан в настройках.")

# Отправка обновления статуса заказа пользователю через Telegram
@receiver(post_save, sender=Order)
def send_order_status_update(sender, instance, **kwargs):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    user = instance.user
    status = instance.get_status_display()

    if hasattr(user, 'profile') and user.profile.telegram_chat_id:
        chat_id = user.profile.telegram_chat_id
        message = f"Ваш заказ #{instance.id} обновлен. Новый статус: {status}."
        try:
            bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления пользователю: {e}")
    else:
        logger.warning("Telegram chat ID не найден у пользователя.")
````

### 🤝 Участие в разработке
1. Форкните репозиторий
2. Создайте feature-ветку (git checkout -b feature/ваша-фича)
3. Закоммитьте изменения (git commit -am 'Добавлена новая фича')
4. Запушьте в ветку (git push origin feature/ваша-фича)
5. Создайте Pull Request


### 📝 Лицензия
#### Этот проект распространяется под лицензией MIT. Подробности смотрите в файле LICENSE.
- Автор: Сергей Орлов – 6202818@gmail.com
- Репозиторий: https://github.com/SergOrloff/FlowerDeliveryMast

### 📞 Контакты
#### Если у вас есть вопросы или предложения, вы можете связаться по электронной почте:
- Email: 6202818@gmail.com

## Спасибо за использование Flower Delivery! 🌸