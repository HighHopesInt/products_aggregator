import tempfile
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
            file = options['file']
            data = open(file, 'r').read()
            temp_file = tempfile.NamedTemporaryFile(mode='w',
                                                    delete=False)
            temp_file.write(data)
            upload_file = UploadedFile()
            print('Done')
            upload_file.file = temp_file.name
            upload_file.save()
            print(temp_file.name)
            temp_file.close()
        else:
            print('You do\'t write arguments')
