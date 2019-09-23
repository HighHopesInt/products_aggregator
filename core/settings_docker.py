#!/usr/bin/env python3
import os

from decouple import config

from .settings import * # noqa

if not os.getenv('BUILD_ON_TRAVIS'):
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('TEST_DB_NAME'),
            'USER': config('TEST_DB_USER'),
            'PASSWORD': config('TEST_DB_PASSWORD'),
            'HOST': config('TEST_DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }

broker_docker = 'amqp://user:password@rabbitmq:5672/'
