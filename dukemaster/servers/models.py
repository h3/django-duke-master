from django.db import models
from django.utils.translation import ugettext_lazy as _


class Server(models.Model):
    name = models.SlugField(u"Name", unique=True, max_length=250)
    hostname = models.CharField(u"Hostname", max_length=250)
    username = models.CharField(u"Username", max_length=250, blank=True, null=True)
    password = models.CharField(u"Password", max_length=250, blank=True, null=True)
    ssh_key = models.TextField(u'SSH key', blank=True, null=True)

    def auth_method(self):
        if self.ssh_key:
            return ('ssh_key', _('SSH key'))
        elif self.username and self.password:
            return ('user_pass', _('Password'))
        else:
            return ('unspecified', _('Unspecified'))

    def __unicode__(self):
        return u"%s" % self.name


class ServerProfile(models.Model):
    name = models.SlugField(u"Name", unique=True, max_length=250)
    commands = models.TextField(u'Commands')

    def __unicode__(self):
        return u"%s" % self.name
