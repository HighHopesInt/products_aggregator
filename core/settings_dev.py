#!/usr/bin/env python3
import os

from decouple import config

from .settings import *  # noqa


if not os.getenv('BUILD_ON_TRAVIS'):
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }

broker_dev = 'amqp://'
