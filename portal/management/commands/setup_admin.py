from django.core.management.base import BaseCommand

from portal.models import User


class Command(BaseCommand):
    help = 'Создает администратора Admin26'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='Admin26',
            defaults={
                'full_name': 'Администратор',
                'phone': '8(999)000-00-00',
                'email': 'admin@uchus.rf',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        user.set_password('Demo20')
        user.save()
        self.stdout.write('Администратор Admin26 / Demo20 готов')
