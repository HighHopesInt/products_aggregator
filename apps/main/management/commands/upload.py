from django.core.management.base import BaseCommand


def upload_file():
    class Command(BaseCommand):
        def handle(self, *args, **options):
            upload_file()
