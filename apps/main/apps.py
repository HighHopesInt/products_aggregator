from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save


class MainConfig(AppConfig):
    name = 'apps.main'

    def ready(self):
        from .models import UploadedFile
        from .signals import dummy, parse_csv_after_upload

        # pre_save.connect(dummy, sender=UploadedFile)
        post_save.connect(parse_csv_after_upload, sender=UploadedFile)
