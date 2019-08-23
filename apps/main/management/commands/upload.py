from django.core.management.base import BaseCommand
from apps.main.utils import upload_files


class Command(BaseCommand):
    help = 'Upload .csv file in DB'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='*', type=str)

    def handle(self, *args, **options):
        try:
            if not options['file']:
                raise ValueError
            for item in options['file']:
                upload_files(item)
        except FileNotFoundError:
            print('Not Found File')
        except ValueError:
            print('Something went wrong')
        except TypeError:
            print('Something went wrong with type')
