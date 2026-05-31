from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User, Application, Review


class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length=6, label='Логин')
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль')
    full_name = forms.CharField(
        label='ФИО',
        validators=[RegexValidator(r'^[А-Яа-яЁё\s]+$', 'Только кириллица и пробелы')]
    )
    phone = forms.CharField(
        max_length=16,
        validators=[RegexValidator(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', 'Формат: 8(XXX)XXX-XX-XX')],
        label='Телефон'
    )
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'phone', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise forms.ValidationError('Логин должен содержать только латиницу и цифры')
        return username


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 3})}