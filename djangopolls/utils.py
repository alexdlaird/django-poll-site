"""
Django is simply a Python library. With Django, the world of Python is at your fingertips, so don't forget
to architect your code around well-defined Python modules.

For example, note that our function below, boring as it may be, is imported into and called from models.py
when Django creates a new "Vote" object.
"""

import hashlib
import time

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2014, Alex Laird'
__version__ = '0.0.1'


def generate_slug():
    return hashlib.sha1(str(time.time())).hexdigest()