import hashlib
import time


def generate_slug():
    return hashlib.sha1(str(time.time())).hexdigest()