# core/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from django.db.models import Sum, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg


# Telegram Bot Integration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class ProductManager(models.Manager):
    def popular(self):
        return self.filter(is_popular=True)

# Модель товара
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('roses', _('Розы')),
        ('tulips', _('Тюльпаны')),
        ('orchids', _('Орхидеи')),
        ('lilies', _('Лилии')),
        ('pions', _('Пионы')),
        ('daisies', _('Ромашки')),
        ('bouquets', _('Букеты')),
        ('other', _('Другие')),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='roses')
    is_popular = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    objects = ProductManager()
    stock = models.PositiveIntegerField(default=0)  # Поле для отслеживания количества на складе
    current_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category)

    def is_in_stock(self, quantity=1):
        return self.stock >= quantity

    def clean(self):
        if self.price <= 0:
            raise ValidationError(_('Цена должна быть положительной.'))
        if self.stock < 0:
            raise ValidationError(_('Количество на складе не может быть отрицательным.'))

    def update_current_rating(self):
        avg_rating = self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        self.current_rating = avg_rating
        self.save(update_fields=['current_rating'])

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')

# Модель корзины
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Корзина пользователя: {self.user.username}"
        return f"Корзина сессии: {self.session}"

    def get_total(self):
        total = self.items.aggregate(total=Sum(F('quantity') * F('product__price')))['total']
        return total if total else 0

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

# Модель элемента корзины
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        verbose_name = _('Элемент корзины')
        verbose_name_plural = _('Элементы корзины')
        unique_together = ('cart', 'product')

# Модель заказа
# core/models.py

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Ожидание')),
        ('confirmed', _('Подтверждено')),
        ('shipped', _('Отправлено')),
        ('delivered', _('Доставлено')),
        ('canceled', _('Отменено')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ {self.id} - {self.status}'

    def get_products_display(self):
        # Получение списка товаров из заказа и форматирование их для отображения в админке
        order_items = self.items.all()
        products = [f"{item.product.name} (x{item.quantity})" for item in order_items]
        return format_html("<br>".join(products))

    get_products_display.short_description = "Товары"

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def colored_status(self):
        status_colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'shipped': 'green',
            'delivered': 'green',
            'canceled': 'red'
        }
        color = status_colors.get(self.status, 'black')
        return format_html(f'<span style="color: {color};">{self.get_status_display()}</span>')

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')


# Модель элемента заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.product.price * self.quantity

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()

    class Meta:
        verbose_name = _('Элемент заказа')
        verbose_name_plural = _('Элементы заказа')

# Модель отзыва
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Отзыв от {self.user} на {self.product}"

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError('Рейтинг должен быть от 1 до 5')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_current_rating()

    class Meta:
        unique_together = ('product', 'user')
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)  # Добавьте это поле

    def __str__(self):
        return self.user.username


class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.PositiveIntegerField()
    total_customers = models.PositiveIntegerField()

    def __str__(self):
        return f"Отчёт за {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = _('Отчёт')
        verbose_name_plural = _('Отчёты')