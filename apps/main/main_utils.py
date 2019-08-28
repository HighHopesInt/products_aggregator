import os

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.main.models import UploadedFile


def save_file(item):
    file = UploadedFile
    if os.path.isdir(item):
        for filename in os.listdir(item):
            with open(item + filename, 'rb') as f:
                data_file = SimpleUploadedFile(name=f.name,
                                               content=f.read())
            file.objects.all().create(file=data_file)
    else:
        with open(item, 'rb') as f:
            data_file = SimpleUploadedFile(name=f.name,
                                           content=f.read())
        file.objects.all().create(file=data_file)
