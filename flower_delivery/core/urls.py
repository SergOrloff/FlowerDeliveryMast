# core\urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import reports_list, reports_list_adm
from .views import sales_report
from .views import popular_products_report, popular_products_report_adm
from .views import sales_report_site, sales_report_site_adm0, generate_sales_report_pdf
from .views import sales_report_site_fig, sales_report_site_adm

urlpatterns = [
    # Основные маршруты каталога и товаров
    path('', views.product_list, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),

    # Маршруты для работы с корзиной
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    # Маршруты для оформления заказа
    path('checkout/', views.checkout, name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_success/', views.order_success, name='order_success'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # Маршруты для работы с пользователями и профилем
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Управление пользователями (администратором)
    path('manage/users/', views.user_list, name='user_list'),
    path('manage/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('manage/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # Управление продуктами (администратором/менеджером)
    path('manage/products/add/', views.add_product, name='add_product'),
    path('manage/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('manage/products/remove/<int:product_id>/', views.remove_product, name='remove_product'),

    # Статические страницы
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

    # Дополнительно: Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Дополнительно: Интеграция с другими функциями
    path("send_message/", views.send_message, name="send_message"),
    path('change_currency/', views.change_currency, name='change_currency'),
    path('repeat_order/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('dadata/suggest-address/', views.suggest_address, name='suggest_address'),
    path('manage/reports/', views.sales_report, name='sales_report'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('sales_report/', sales_report, name='sales_report'),
    path('download_sales_report_csv/', views.download_sales_report_csv, name='download_sales_report_csv'),
    path('reports/popular-products/', popular_products_report, name='popular_products_report'),
    path('reports/sales_report_site/', sales_report_site, name='sales_report_site'),
    path('reports/sales_report_site_fig/', sales_report_site_fig, name='sales_report_site_fig'),
    path('reports/sales_report_site_adm/', sales_report_site_adm, name='sales_report_site_adm'),
    path('reports/sales_report_site_adm0/', sales_report_site_adm0, name='sales_report_site_adm0'),
    path('reports/reports_list_adm/', reports_list_adm, name='reports_list_adm'),
    path('reports/popular_products_report_adm/', popular_products_report_adm, name='popular_products_report_adm'),
    path('reports/', reports_list, name='reports_list'),
    path('reports/sales/download/csv/', views.download_sales_report_csv, name='download_sales_report_csv'),
    path('generate_sales_report_pdf/', generate_sales_report_pdf, name='generate_sales_report_pdf'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/history/', views.order_history, name='order_history'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('rate_product/<int:product_id>/', views.rate_product, name='rate_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

