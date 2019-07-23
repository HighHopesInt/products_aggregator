from django.core.management.base import BaseCommand
from apps.main.tasks import parse


class Command(BaseCommand):

    help = 'Uploaded file in DataBase'

    def handle(self, *args, **options):
        if options['file']:
            parse()

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            action='store_true',
            default=False,
            help='The upload file'
        )
