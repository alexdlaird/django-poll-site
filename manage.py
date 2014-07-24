#!/usr/bin/env python

"""
Start here. Execute this script with "python manage.py help" for a list of options available
to you from Django.

To get started tinkering with development, execute "python manage.py runserver" to start a
development web server, which will allow you to access your Django application by pointing
your browser to http://localhost:8000.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopollsite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
