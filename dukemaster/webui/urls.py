from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

urlpatterns=patterns('',
    url(r'command/$', 'dukemaster.webui.views.command', name='dukemaster-command'),
)
