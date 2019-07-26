import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from apps.main.models import UploadedFile


class Command(BaseCommand):
    help = 'Upload .csv file in DB'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='*', type=str)

    def handle(self, *args, **options):
        try:
            if not options['file']:
                raise ValueError
            for item in options['file']:
                if os.path.isdir(item):
                    for filename in os.listdir(item):
                        with open(item + filename, 'rb') as f:
                            data_file = SimpleUploadedFile(name=f.name,
                                                           content=f.read())
                        UploadedFile.objects.all().create(file=data_file)
                else:
                    with open(item, 'rb') as f:
                        data_file = SimpleUploadedFile(name=f.name,
                                                       content=f.read())
                    UploadedFile.objects.all().create(file=data_file)
        except FileNotFoundError:
            print('Not Found File')
        except ValueError:
            print('Something went wrong')
        except TypeError:
            print('Something went wrong with type')
