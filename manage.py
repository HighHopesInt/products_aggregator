#!/usr/bin/env python
import os
import sys
import dotenv
import environ

import core.settings_dev

if __name__ == "__main__":
    env = environ.Env()
    project_path = os.path.dirname(os.path.abspath(__file__))

    dotenv.read_dotenv(os.path.join(project_path, '.env'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          env('DJANGO_SETTINGS_MODULE',
                              default=core.settings_dev))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
