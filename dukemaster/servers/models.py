from django.db import models


class Server(models.Model):
    name = models.SlugField(u"Name", unique=True, max_length=250)
    hostname = models.Charfield(u"Hostname", max_length=250)
    username = models.Charfield(u"Username", max_length=250)
    password = models.Charfield(u"Password", max_length=250)
    ssh_key = models.TextField(u'SSH key')


class ServerProfile(models.Model):
    name = models.SlugField(u"Name", unique=True, max_length=250)
    commands = models.TextField(u'Commands')
