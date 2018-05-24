from django.db import transaction

from core import celery_app
# from .tasks import parse


def dummy(sender, instance, created, **kwargs):
    pass
    # print('ok')


def parse_csv_after_upload(sender, instance, created, **kwargs):
    if created:
        # parse.delay(instance.id)
        # transaction.on_commit(lambda: parse.delay(instance.id))

        # celery_app.send_task('apps.main.tasks.parse', [instance.id])
        transaction.on_commit(lambda: celery_app.send_task(
            'apps.main.tasks.parse', [instance.id]
        ))
