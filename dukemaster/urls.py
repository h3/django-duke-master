from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/',     include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
   #(r'^i18n/',      include('django.conf.urls.i18n')),
    (r'^%s(.*)$' % settings.STATIC_URL[1:], 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
