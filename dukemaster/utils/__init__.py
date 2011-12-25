"""
dukemaster.utils
~~~~~~~~~~~~~~~~

Taken from Sentry utils
https://github.com/dcramer/django-sentry/blob/master/sentry/utils/__init__.py

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

def is_float(var):
    try:
        float(var)
    except ValueError:
        return False
    return True

def get_signature(message, timestamp):
    return hmac.new(settings.KEY, '%s %s' % (timestamp, message), sha_constructor).hexdigest()

def get_auth_header(signature, timestamp, client):
    return 'Sentry sentry_signature=%s, sentry_timestamp=%s, sentry_client=%s' % (
        signature,
        timestamp,
        sentry.VERSION,
    )

def parse_auth_header(header):
    return dict(map(lambda x: x.strip().split('='), header.split(' ', 1)[1].split(',')))
