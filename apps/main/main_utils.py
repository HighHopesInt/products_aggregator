import os

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.main.models import UploadedFile


def open_file(file_upload, file_directory=''):
    """
    File_directory use when we want to upload files in directory.
    If we want upload simple list files file_directory must be empty.
    """
    file = UploadedFile
    with open(file_upload + file_directory, 'rb') as f:
        data_file = SimpleUploadedFile(name=f.name,
                                       content=f.read())
    file.objects.all().create(file=data_file)


def save_file(item):
    if os.path.isdir(item):
        for filename in os.listdir(item):
            open_file(item, file_directory=filename)
    else:
        open_file(item)
