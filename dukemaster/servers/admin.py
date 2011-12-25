# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from dukemaster.servers.models import *

#class DraftWinnerInline(admin.TabularInline):
#    model = DraftWinner
#    extra = 0
#    readonly_fields =  ('firstname',  'user', 'points', 'position', 'email')


class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'get_auth_method', 'username')

    def get_auth_method(self, obj):
        return obj.auth_method()[1]
    get_auth_method.short_description = _('Auth. method')
   #get_auth_method.allow_tags = True
#   readonly_fields =  ('date',)
#   inlines = [DraftWinnerInline]
#   date_hierarchy = 'date'
#   search_fields = ['draftwinner__user__username']
#   list_filter = ['email_sent']

#   def has_add_permission(self, request):
#       return False
admin.site.register(Server, ServerAdmin)


class ServerProfileAdmin(admin.ModelAdmin):
    list_display =  ('name',)
#   readonly_fields =  ('draft', 'firstname',  'user', 'points', 'position', 'email')
#   search_fields = ['firstname', 'user__username', 'email']
#   list_filter = ['draft']
#   date_hierarchy = 'draft'

#   def has_add_permission(self, request):
#      return False
admin.site.register(ServerProfile, ServerProfileAdmin)

