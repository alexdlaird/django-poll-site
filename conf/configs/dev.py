"""
Settings for a development environment.
"""

# Import system modules
import os
import warnings

# Import project modules
from .common import DEFAULT_TEMPLATE_CONTEXT_PROCESSORS, DEFAULT_MIDDLEWARE_CLASSES, DEFAULT_INSTALLED_APPS

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2014, Alex Laird'
__version__ = '0.0.1'


# Define the base working directory of the application
BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))


# Application definition

INSTALLED_APPS = DEFAULT_INSTALLED_APPS

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.debug',
)


#############################
# Django configuration
#############################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i!^ep&$gc*5@+=c%l4cmpiiv-svssaz5)@h47m=%zdoe*rt^1q'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost',
                 '127.0.0.1']

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
        'djangopolls_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'djangopolls_log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'djangopolls': {
            'handlers': ['console', 'djangopolls_log'],
            'level': 'DEBUG',
        },
    }
}

# When in development, we want to be warned about dates that don't have a timezone
warnings.filterwarnings('error', r"DateTimeField .* received a naive datetime", RuntimeWarning,
                        r'django\.db\.models\.fields')


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


# For testing we'll spit emails out to the console, but comment out the console backend and uncomment and
# supply valid credentials for the SMTP backend to observer Django's use of an SMTP email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'