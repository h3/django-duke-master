#!/usr/bin/env python

"""
Largely from django-sentry

https://github.com/dcramer/django-sentry/blob/master/sentry/scripts/runner.py

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

"""

from __future__ import with_statement
import eventlet
import errno
import imp
import logging
import os
import os.path
import sys

from daemon.daemon import DaemonContext
from daemon.runner import DaemonRunner, make_pidlockfile
from django.conf import settings as django_settings
from django.core.management import call_command
from eventlet import wsgi
from optparse import OptionParser

import dukemaster

DUKEMASTER_ROOT = os.path.dirname(os.path.abspath(dukemaster.__file__))

KEY_LENGTH = 40

SETTINGS_TEMPLATE = """
import os.path

from dukemaster.conf.server import *

ROOT = os.path.dirname(__file__)

DATABASES = {
'default': {
# You can swap out the engine for MySQL easily by changing this value
# to ``django.db.backends.mysql`` or to PostgreSQL with
# ``django.db.backends.postgresql_psycopg2``
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(ROOT, 'dukemaster.db'),
'USER': 'postgres',
'PASSWORD': '',
'HOST': '',
'PORT': '',
}
}

DUKEMASTER_KEY = %(default_key)r

# Set this to false to require authentication
DUKEMASTER_PUBLIC = False

DUKEMASTER_WEB_HOST = '0.0.0.0'
DUKEMASTER_WEB_PORT = 9000

DUKEMASTER_WEB_LOG_FILE = os.path.join(ROOT, 'dukemaster.log')
DUKEMASTER_WEB_PID_FILE = os.path.join(ROOT, 'dukemaster.pid')
"""

def copy_default_settings(filepath):
    """
Creates a default settings file at ``filepath``.
"""
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filepath, 'w') as fp:
        key = os.urandom(KEY_LENGTH)

        output = SETTINGS_TEMPLATE % dict(default_key=key)
        fp.write(output)

def settings_from_file(filename, silent=False):
    """
Configures django settings from an arbitrary (non sys.path) filename.
"""
    mod = imp.new_module('config')
    mod.__file__ = filename
    try:
        execfile(filename, mod.__dict__)
    except IOError, e:
        if silent and e.errno in (errno.ENOENT, errno.EISDIR):
            return False
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise

    tuple_settings = ("INSTALLED_APPS", "TEMPLATE_DIRS")

    if not django_settings.configured:
        django_settings.configure()

    for setting in dir(mod):
        if setting == setting.upper():
            setting_value = getattr(mod, setting)
            if setting in tuple_settings and type(setting_value) == str:
                setting_value = (setting_value,) # In case the user forgot the comma.
            setattr(django_settings, setting, setting_value)


class DukeMasterServer(DaemonRunner):
    pidfile_timeout = 10
    start_message = u"started with pid %(pid)d"

    def __init__(self, host=None, port=None, pidfile=None,
                 logfile=None, daemonize=False, debug=False):
        from dukemaster.conf import settings

        if not logfile:
            logfile = settings.WEB_LOG_FILE

        logfile = os.path.realpath(logfile)
        pidfile = os.path.realpath(pidfile or settings.WEB_PID_FILE)

        if daemonize:
            detach_process = True
        else:
            detach_process = False

        self.daemon_context = DaemonContext(detach_process=detach_process)
        self.daemon_context.stdout = open(logfile, 'w+')
        self.daemon_context.stderr = open(logfile, 'w+', buffering=0)

        self.debug = debug
        self.pidfile = make_pidlockfile(pidfile, self.pidfile_timeout)

        self.daemon_context.pidfile = self.pidfile

        self.host = host or settings.WEB_HOST
        self.port = port or settings.WEB_PORT

        # HACK: set app to self so self.app.run() works
        self.app = self

    def execute(self, action):
        self.action = action

        # Upgrade needs to happen before forking
        upgrade()

        if self.daemon_context.detach_process is False and self.action == 'start':
            # HACK:
            self.run()
        else:
            self.do_action()

    def run(self):
        from dukemaster.wsgi import application

        def inner_run():
            wsgi.server(eventlet.listen((self.host, self.port)), application)

        if self.debug:
            from django.utils import autoreload
            autoreload.main(inner_run)
        else:
            inner_run()


def upgrade(interactive=True):
    from dukemaster.conf import settings

    call_command('syncdb', database=settings.DATABASE_USING or 'default', interactive=interactive)

    if 'south' in django_settings.INSTALLED_APPS:
        call_command('migrate', database=settings.DATABASE_USING or 'default', interactive=interactive)

def main():
    command_list = ('start', 'stop', 'restart', 'upgrade')
    args = sys.argv
    if len(args) < 2 or args[1] not in command_list:
        print "usage: dukemaster [command] [options]"
        print
        print "Available subcommands:"
        for cmd in command_list:
            print " ", cmd
        sys.exit(1)

    parser = OptionParser(version="%%prog %s" % dukemaster.VERSION)
    parser.add_option('--config', metavar='CONFIG')
    if args[1] == 'start':
        parser.add_option('--host', metavar='HOSTNAME')
        parser.add_option('--port', type=int, metavar='PORT')
        parser.add_option('--daemon', action='store_true', default=False, dest='daemonize')
        parser.add_option('--no-daemon', action='store_false', default=False, dest='daemonize')
        parser.add_option('--debug', action='store_true', default=False, dest='debug')
        parser.add_option('--pidfile', dest='pidfile')
        parser.add_option('--logfile', dest='logfile')
    elif args[1] == 'stop':
        parser.add_option('--pidfile', dest='pidfile')
        parser.add_option('--logfile', dest='logfile')

    (options, args) = parser.parse_args()

    if options.config:
        # assumed to be a file
        config_path = options.config
    else:
        config_path = os.path.expanduser(os.path.join('~', '.dukemaster', 'dukemaster.conf.py'))

    if not os.path.exists(config_path):
        try:
            copy_default_settings(config_path)
        except OSError, e:
            raise e.__class__, 'Unable to write default settings file to %r' % config_path

    settings_from_file(config_path)

    if getattr(options, 'debug', False):
        django_settings.DEBUG = True

    if args[0] == 'upgrade':
        upgrade()

    elif args[0] == 'start':

        if not os.path.exists(os.path.join(DUKEMASTER_ROOT, 'static/')):
            from dukemaster.conf import settings
            call_command('collectstatic', 
                    database=settings.DATABASE_USING or 'default', 
                    interactive=False)
        app = DukeMasterServer(host=options.host, port=options.port,
                           pidfile=options.pidfile, logfile=options.logfile,
                           daemonize=options.daemonize, debug=options.debug)
        app.execute(args[0])

    elif args[0] == 'restart':
        app = DukeMasterServer()
        app.execute(args[0])

    elif args[0] == 'stop':
        app = DukeMasterServer(pidfile=options.pidfile, logfile=options.logfile)
        app.execute(args[0])

    sys.exit(0)

if __name__ == '__main__':
    main()
