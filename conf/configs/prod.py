"""
Settings for a production environment.

In a forked repository, prod.py should never be committed to the repository. It should
be maintained in a secure location, and you should update fabfile.py to move the prod.py
conf file into place only in a production environment.
"""

# Import system modules
import os

# Import project modules
from .common import DEFAULT_TEMPLATE_CONTEXT_PROCESSORS, DEFAULT_MIDDLEWARE_CLASSES, DEFAULT_INSTALLED_APPS

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2014, Alex Laird'
__version__ = '0.0.1'


# Define the base working directory of the application
BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))


# Application definition

INSTALLED_APPS = DEFAULT_INSTALLED_APPS

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS


#############################
# Django configuration
#############################

# Security

SECRET_KEY = 'ui(0mu1=%8pfnnuy0i&8dlf*whlfo4_u6&4mlm)c90aoj1_etn'

ALLOWED_HOSTS = ['www.myserver.com',
                 'myserver.com']

# Logging

ADMINS = (
    ('My Project', 'project@myserver.com')
)
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'django_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'djangopolls_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'djangopolls_log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['django_log', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'djangopolls': {
            'handlers': ['djangopolls_log', 'mail_admins'],
            'level': 'INFO',
        },
    }
}

# Database

DATABASES = {
    'default': {
        'NAME': 'djangopolls',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db_host',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


# For testing we'll spit emails out to the console, but comment out the console backend and uncomment and
# supply valid credentials for the SMTP backend to observer Django's use of an SMTP email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.myserver.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sender@myserver.com'
EMAIL_HOST_PASSWORD = 'mysupersecretpassword'