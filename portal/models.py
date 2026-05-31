

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=16, validators=[RegexValidator(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$')])


class Application(models.Model):
    COURSE_CHOICES = [
        ('Основы алгоритмизации и программирования', 'Основы алгоритмизации и программирования'),
        ('Основы веб-дизайна', 'Основы веб-дизайна'),
        ('Основы проектирования баз данных', 'Основы проектирования баз данных'),
    ]
    STATUS = [
        ('Новая', 'Новая'),
        ('Идет обучение', 'Идет обучение'),
        ('Обучение завершено', 'Обучение завершено'),
    ]
    PAYMENT = [
        ('наличными', 'Наличными'),
        ('перевод по номеру телефона', 'Перевод по номеру телефона'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    start_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT)
    status = models.CharField(max_length=50, choices=STATUS, default='Новая')
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
