"""
WSGI config for djangopollsite project.

It exposes the WSGI callable as a module-level variable named ``application``. When you're
ready to begin implemention a production-like environment for your application (plugging a
real web server, like Apache or Nginx, into Django), you'll want to check out Django's
WSGI documentation and point your web server's host configuration at this file.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopolls.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
