import base64
import logging

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from dukemaster.servers.models import Server
from dukemaster.utils.compat import pickle

class GzippedDictField(models.TextField):
    """
Slightly different from a JSONField in the sense that the default
value is a dictionary.

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, basestring) and value:
            try:
                value = pickle.loads(base64.b64decode(value).decode('zlib'))
            except Exception, e:
                logger.exception(e)
                return {}
        elif not value:
            return {}
        return value

    def get_prep_value(self, value):
        if value is None:
            return
        return base64.b64encode(pickle.dumps(transform(value)).encode('zlib'))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class CommandLog(models.Model):
    command = models.CharField(u"Command", max_length=250, db_index=True)
    arguments = models.TextField(u"Arguments", blank=True, null=True)
    output  = models.TextField(u"Output", blank=True, null=True)
    ip_address = models.IPAddressField(u"IP address", blank=True, null=True, db_index=True)
    username = models.CharField(u"Username", max_length=150, db_index=True)
    server = models.CharField(u"Server", max_length=150, db_index=True)
    datetime = models.DateTimeField(default=datetime.now, db_index=True)
    raw = GzippedDictField(u"Raw request")

    def __unicode__(self):
        return u"%s@%s: %s %s" % (self.user, self.command, self.arguments or '')
