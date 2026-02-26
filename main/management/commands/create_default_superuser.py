from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a default superuser (non-interactive).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
            help='Username for the superuser'
        )
        parser.add_argument(
            '--email',
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
            help='Email for the superuser'
        )
        parser.add_argument(
            '--password',
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass'),
            help='Password for the superuser'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='If set, will delete any existing user with the same username and recreate as superuser'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']
        force = options['force']

        existing = User.objects.filter(username=username).first()
        if existing:
            if existing.is_superuser:
                if not force:
                    self.stdout.write(self.style.WARNING(
                        f"Superuser '{username}' already exists. Use --force to recreate."
                    ))
                    return
                existing.delete()
                self.stdout.write(self.style.WARNING(
                    f"Deleted existing superuser '{username}' (recreating)."
                ))
            else:
                if not force:
                    self.stdout.write(self.style.ERROR(
                        f"User '{username}' exists and is not a superuser. Use --force to replace."
                    ))
                    return
                existing.delete()
                self.stdout.write(self.style.WARNING(
                    f"Deleted existing user '{username}' (recreating as superuser)."
                ))

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
