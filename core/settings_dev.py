#!/usr/bin/env python3
from .settings import * # noqa
import environ
import os

env = environ.Env()


if os.getenv('BUILD_ON_TRAVIS', False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
        }
    }
else:
    DATABASES = {
       'default': {
           'ENGINE': env.str('DB_ENGINE'),
           'NAME': env.str('DB_NAME'),
           'USER': env.str('DB_USER'),
           'PASSWORD': env.str('DB_PASSWORD'),
           'HOST': env.str('DB_HOST'),
           'PORT': env.str('DB_PORT'),
       }
    }
