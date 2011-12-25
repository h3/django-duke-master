# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from dukemaster.webui.models import *


class CommandLogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'username', 'server', 'command', 'arguments')
    readonly_fields =  ('command', 'username', 'server', 'command', 'datetime', 'arguments')
    date_hierarchy = 'datetime'
    search_fields = ['command', 'username', 'server', 'ip_address']
    list_filter = ['command', 'username', 'server', 'ip_address']

    def has_add_permission(self, request):
        return False
admin.site.register(CommandLog, CommandLogAdmin)
