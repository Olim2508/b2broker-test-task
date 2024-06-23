import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser if one does not exist"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.environ.get("SUPERUSER_USERNAME", "admin"),
                email=os.environ.get("SUPERUSER_EMAIL", "admin@gmail.com"),
                password=os.environ.get("SUPERUSER_PASSWORD", "admin"),
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))
