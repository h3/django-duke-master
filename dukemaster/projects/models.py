from django.db import models


class Project(models.Model):
    name = models.Charfield(u"Name", max_length=250)


class ProjectSource(models.Model):
    url = models.Charfield(u"Source URL", max_length=250)
    project = models.OneToOneField(Project)

class ProjectTemplate(models.Model):
    name = models.Charfield(u"Name", max_length=250)
    url = models.Charfield(u"Source URL", max_length=250)
