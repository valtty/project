from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=16,
        validators=[RegexValidator(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$')],
    )


class Application(models.Model):
    COURSE_CHOICES = [
        ('Курсы повышения квалификации', 'Курсы повышения квалификации'),
        ('Курсы переподготовки', 'Курсы переподготовки'),
        ('Курсы по охране труда', 'Курсы по охране труда'),
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

    def status_css_class(self):
        if self.status == 'Новая':
            return 'status-new'
        if self.status == 'Идет обучение':
            return 'status-progress'
        if self.status == 'Обучение завершено':
            return 'status-done'
        return ''

    def can_leave_review(self):
        return self.status == 'Обучение завершено' and not hasattr(self, 'review')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
