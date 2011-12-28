from django.db import models
from dukemaster.servers.models import Server

# TODO: dynamic (with plugin architecture)
REPOSITORY_TYPES = (
    ('git', 'Git'),
    ('svn', 'Subversion'),
)


class Project(models.Model):
    name = models.CharField(u"Name", max_length=250)

    def __unicode__(self):
        return u"%s" % self.name


class ProjectSource(models.Model):
    url = models.CharField(u"Source URL", max_length=250)
    protocol = models.CharField(u"Type", max_length=5, choices=REPOSITORY_TYPES, default="git")
    project = models.OneToOneField(Project)
    password = models.CharField(u"Password", max_length=250, blank=True, null=True)
    ssh_key = models.CharField(u"SSH key", max_length=250, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.url


class ProjectStage(models.Model):
    server  = models.ForeignKey(Server)
    project = models.ForeignKey(Project)
    is_prod = models.BooleanField(u"Is production", default=False)

    def __unicode__(self):
        return u"%s - %s" % (self.server, self.project)


class ProjectTemplate(models.Model):
    name = models.CharField(u"Name", max_length=250)
    url = models.CharField(u"Source URL", max_length=250)

    def __unicode__(self):
        return u"%s" % self.name
