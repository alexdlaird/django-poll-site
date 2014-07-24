"""
Django is simply a Python library. With Django, the world of Python is at your fingertips, so don't forget
to architect your code around well-defined Python modules.

For example, note that our function below, boring as it may be, is imported into and called from models.py
when Django creates a new "Vote" object.
"""

import hashlib
import time


def generate_slug():
    return hashlib.sha1(str(time.time())).hexdigest()