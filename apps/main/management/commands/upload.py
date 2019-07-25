from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from apps.main.models import UploadedFile


class Command(BaseCommand):
    help = 'Upload .csv file in DB'

    def add_arguments(self, parser):
        parser.add_argument('--file',
                            '-f',
                            help='File to be upload',
                            type=str)

    def handle(self, *args, **options):
        if options['file']:
            with open(options['file'], 'rb') as f:
                data_file = SimpleUploadedFile(name=f.name, content=f.read())
            UploadedFile.objects.all().create(file=data_file)
        else:
            print('You do\'t write arguments')
