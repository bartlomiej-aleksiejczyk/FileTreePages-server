import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser if one does not already exist"

    def handle(self, *args, **kwargs):
        user = get_user_model()

        superuser_username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        superuser_email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        superuser_password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not user.objects.filter(username=superuser_username).exists():
            user.objects.create_superuser(
                username=superuser_username,
                email=superuser_email,
                password=superuser_password,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {superuser_username} created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {superuser_username} already exists")
            )
