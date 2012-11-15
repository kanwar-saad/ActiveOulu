from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'activeoulu.views.home', name='home'),
    # url(r'^activeoulu/', include('activeoulu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    (r'^btscan/$', 'web_app.views.btScan'),
    (r'^api/bt_devices/$', 'web_app.views.btDevices'),
    (r'^api/bt_activity/$', 'web_app.views.btActivity'),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
    )



urlpatterns += staticfiles_urlpatterns()
