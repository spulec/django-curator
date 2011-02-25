import os

from django.conf.urls.defaults import *

DASHBOARD_ROOT = os.path.dirname(__file__)

# place app url patterns here
urlpatterns = patterns('',
    url(r'^_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(DASHBOARD_ROOT, 'media')}, name='dashboard-media'),

    #(r'^$', 'home', name='dashboard'),
    url(r'^widget/(?P<widget_id>\d+)/$', 'dashboard.views.widget'),
    url(r'^(?P<dashboard_name>\w+)/$', 'dashboard.views.dashboard'),
    url(r'^(?P<dashboard_name>\w+)/order/$', 'dashboard.views.widget_order', name='widget_order'),
)
