"""
dukemaster.conf.settings
~~~~~~~~~~~~~~~~~~~~~~~~

Note: These settings are largely taken from django sentry

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from dukemaster.conf.defaults import *

from django.conf import settings
from django.utils.hashcompat import md5_constructor
from django.utils.translation import ugettext_lazy as _

import warnings

# Some sane overrides to better mix with Django
DEBUG = getattr(settings, 'DEBUG', False) and not getattr(settings, 'DUKEMASTER_TESTING', False)
KEY = getattr(settings, 'DUKEMASTER_KEY', md5_constructor(settings.SECRET_KEY).hexdigest())
EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAIL_SUBJECT_PREFIX', EMAIL_SUBJECT_PREFIX)
INTERNAL_IPS = getattr(settings, 'INTERNAL_IPS', INTERNAL_IPS)
SERVER_EMAIL = getattr(settings, 'SERVER_EMAIL', SERVER_EMAIL)

for k in dir(settings):
    if k.startswith('DUKEMASTER'):
        locals()[k.split('DUKEMASTER_', 1)[1]] = getattr(settings, k)

LOG_LEVELS = [(k, _(v)) for k, v in LOG_LEVELS]

if locals().get('REMOTE_URL'):
    if isinstance(REMOTE_URL, basestring):
        SERVERS = [REMOTE_URL]
    elif not isinstance(REMOTE_URL, (list, tuple)):
        raise ValueError("Dukemaster setting 'REMOTE_URL' must be of type list.")

if locals().get('REMOTE_TIMEOUT'):
    TIMEOUT = REMOTE_TIMEOUT

def configure(**kwargs):
    for k, v in kwargs.iteritems():
        if k.upper() != k:
            warnings.warn('Invalid setting, \'%s\' which is not defined by Dukemaster' % k)
        else:
            locals[k] = v


