#!/usr/bin/env python
import os
import sys

from decouple import config

from docker_runtime import in_docker

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.abspath(__file__))
    docker = in_docker()
    if os.getenv('BUILD_ON_TRAVIS'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'core.settings_ci')
    elif docker:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              config('DOCKER_DJANGO_SETTINGS_MODULE',
                                     default='core.settings_docker'))
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              config('DJANGO_SETTINGS_MODULE',
                                     default='core.settings_dev'))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
