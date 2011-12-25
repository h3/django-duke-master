"""
dukemaster.utils.compat
~~~~~~~~~~~~~~~~~~~~~~~

Taken from django-sentry

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

try:
    import cPickle as pickle
except ImportError:
    import pickle
