#!/usr/bin/env python3
from __future__ import absolute_import, unicode_literals
import os
import dotenv
import environ
from celery import Celery

env = environ.Env()

# set the default Django settings module for the 'celery' program.
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.getenv('BUILD_ON_TRAVIS'):
    dotenv.read_dotenv(os.path.join(project_path, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')

app = Celery('core', broker='amqp://', include=['apps.main.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
