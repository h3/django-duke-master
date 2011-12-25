"""
dukemaster.utils
~~~~~~~~~~~~~~~~

Taken from Sentry utils
https://github.com/dcramer/django-sentry/blob/master/sentry/utils/__init__.py

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
import hmac
import logging
try:
    import pkg_resources
except ImportError:
    pkg_resources = None
import sys
import uuid
from pprint import pformat
from types import ClassType, TypeType

import django
from django.conf import settings as django_settings
from django.http import HttpRequest
from django.utils.encoding import force_unicode
from django.utils.functional import Promise
from django.utils.hashcompat import md5_constructor, sha_constructor

import dukemaster
from dukemaster.conf import settings

def is_float(var):
    try:
        float(var)
    except ValueError:
        return False
    return True

def get_signature(message, timestamp):
    return hmac.new(settings.KEY, '%s %s' % (timestamp, message), sha_constructor).hexdigest()

def get_auth_header(signature, timestamp, client):
    return 'Dukemaster duke_signature=%s, duke_timestamp=%s, duke_client=%s' % (
        signature,
        timestamp,
        dukemaster.VERSION,
    )

def parse_auth_header(header):
    return dict(map(lambda x: x.strip().split('='), header.split(' ', 1)[1].split(',')))
