from django.apps import AppConfig
from django.db.models.signals import post_save


class MainConfig(AppConfig):
    name = 'apps.main'

    def ready(self):
        from .models import UploadedFile
        from .signals import parse_csv_after_upload

        post_save.connect(parse_csv_after_upload, sender=UploadedFile)
