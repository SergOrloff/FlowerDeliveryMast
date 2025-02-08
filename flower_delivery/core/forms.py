# core/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Product, Review
from django.contrib.auth.forms import UserCreationForm
from dadata import Dadata
from django.conf import settings
import logging
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

logger = logging.getLogger(__name__)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Телефон",
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона.")],
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона', 'class': 'form-control'}),
    )
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label="ФИО",
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше полное имя', 'class': 'form-control'}),
    )
    delivery_address = forms.CharField(
        max_length=255,
        required=True,
        label="Адрес доставки",
        widget=forms.TextInput(attrs={'placeholder': 'Введите адрес доставки', 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['phone']
            profile.full_name = self.cleaned_data['full_name']
            profile.delivery_address = self.cleaned_data['delivery_address']
            profile.save()
        return user

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False, label="Телефон")
    full_name = forms.CharField(max_length=255, required=False, label="ФИО")
    delivery_address = forms.CharField(max_length=255, required=False, label="Адрес доставки")

    class Meta:
        model = UserProfile
        fields = ['phone', 'full_name', 'delivery_address']

class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False, label="Телефон")
    full_name = forms.CharField(max_length=255, required=False, label="ФИО")
    delivery_address = forms.CharField(max_length=255, required=False, label="Адрес доставки")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'profile'):
            self.fields['phone'].initial = user.profile.phone
            self.fields['full_name'].initial = user.profile.full_name
            self.fields['delivery_address'].initial = user.profile.delivery_address

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = self.cleaned_data['phone']
        profile.full_name = self.cleaned_data['full_name']
        profile.delivery_address = self.cleaned_data['delivery_address']
        if commit:
            profile.save()
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AddressForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        label='Адрес',
        widget=forms.TextInput(attrs={'placeholder': 'Введите адрес', 'class': 'form-control'})
    )

    def clean_address(self):
        address = self.cleaned_data['address']
        try:
            dadata = Dadata(settings.DADATA_API_KEY, settings.DADATA_SECRET_KEY)
            result = dadata.suggest("address", address)
            if result and len(result) > 0:
                return result[0]['value']
        except Exception as e:
            logger.error(f"Ошибка при подключении к DaData: {e}")
            raise forms.ValidationError(_("Не удалось определить адрес. Пожалуйста, проверьте введённые данные."))
        finally:
            dadata.close()

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SalesReportForm(forms.Form):
    start_date = forms.DateField(
        label='Начало периода',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='Конец периода',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        label='Рейтинг',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True})
    )
    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Оставьте ваш отзыв...', 'rows': 5, 'required': True})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
