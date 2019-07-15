#!/usr/bin/env python3
from .settings import *
import environ

env = environ.Env()

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
