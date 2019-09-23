#!/usr/bin/env python3
from __future__ import absolute_import, unicode_literals
import os

import environ
from celery import Celery
from decouple import config

from docker_runtime import in_docker
from core.settings_dev import broker_dev
from core.settings_docker import broker_docker
from core.settings_ci import broker_ci

env = environ.Env()

# set the default Django settings module for the 'celery' program.
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docker = in_docker()
if os.getenv('BUILD_ON_TRAVIS'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'core.settings_ci')
    broker = broker_ci
elif docker:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          config('DOCKER_DJANGO_SETTINGS_MODULE',
                                 default='core.settings_docker'))
    broker = broker_docker
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          config('DJANGO_SETTINGS_MODULE',
                                 default='core.settings_dev'))
    broker = broker_dev

app = Celery('core',
             broker=broker,
             include=['apps.main.tasks', 'apps.scraper.tasks'],
             backend='rpc://')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
