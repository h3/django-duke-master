# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from dukemaster.projects.models import *


class ProjectSourceInline(admin.TabularInline):
    model = ProjectSource
    extra = 0


class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
#   readonly_fields =  ('date',)
    inlines = [ProjectSourceInline, ProjectStageInline]
#   date_hierarchy = 'date'
#   search_fields = ['draftwinner__user__username']
#   list_filter = ['email_sent']

#   def has_add_permission(self, request):
#       return False
admin.site.register(Project, ProjectAdmin)


class ProjectTemplateAdmin(admin.ModelAdmin):
    list_display =  ('name', 'url')
admin.site.register(ProjectTemplate, ProjectTemplateAdmin)


