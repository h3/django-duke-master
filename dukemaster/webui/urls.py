from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from unicheckin.website.views import *

urlpatterns=patterns('',
    # Public views
   #url(r'^$',              HomeView.as_view(),         name='website-home'),
)
