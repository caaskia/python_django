from django.contrib.auth.models import User, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)

        permission_logentry = Permission.objects.get(
            codename='view_logentry'
        )
        # добавление разрешения в группу

        # связать пользователя напрямую с разрешением
        user.user_permissions.add(permission_logentry)

        user.save()