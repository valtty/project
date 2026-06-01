import re
from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import User, Application, Review


class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length=6, label='Логин')
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль')
    full_name = forms.CharField(
        label='ФИО',
        validators=[RegexValidator(r'^[А-Яа-яЁё\s]+$', 'Только кириллица и пробелы')],
    )
    phone = forms.CharField(
        max_length=16,
        validators=[RegexValidator(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', 'Формат: 8(XXX)XXX-XX-XX')],
        label='Телефон',
    )
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'phone', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r'[A-Za-z0-9]+', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username


class ApplicationForm(forms.ModelForm):
    start_date = forms.CharField(
        label='Дата начала обучения',
        widget=forms.TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
    )

    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']

    def clean_start_date(self):
        value = self.cleaned_data.get('start_date', '').strip()
        try:
            return datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise forms.ValidationError('Укажите дату в формате ДД.ММ.ГГГГ')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 3})}
