"""
dukemaster.utils
~~~~~~~~~~~~~~~~

Taken from Sentry utils
https://github.com/dcramer/django-sentry/blob/master/sentry/utils/__init__.py

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
import hmac

from hashlib import sha1


def is_float(var):
    try:
        float(var)
    except ValueError:
        return False
    return True

def get_signature(key, message, timestamp):
    return hmac.new(key, '%s %s' % (timestamp, message), sha1).hexdigest()

def parse_auth_header(header):
    return dict(map(lambda x: x.strip().split('='), header.split(' ', 1)[1].split(',')))
