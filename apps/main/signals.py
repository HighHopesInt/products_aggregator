from .load_csv import parse


def dummy(sender, instance, created, **kwargs):
    pass
    # print('ok')


def parse_csv_after_upload(sender, instance, created, **kwargs):
    if created:
        parse(instance)
