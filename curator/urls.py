import os

from django.conf.urls.defaults import *

DASHBOARD_ROOT = os.path.dirname(__file__)

# place app url patterns here
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(DASHBOARD_ROOT, 'media')}, name='curator-media'),

    #(r'^$', 'home', name='dashboard'),
    
    url(r'^widget/(?P<widget_id>\d+)/$', 'curator.views.widget', name='widget_view'),
    url(r'^widget/(?P<widget_id>\d+)/data$', 'curator.views.widget_data', name='widget_data'),
    url(r'^widget_size/$', 'curator.views.widget_size', name='widget_size'),
    url(r'^model_fields/(?P<model_name>[.\w]+)/$', 'curator.views.model_fields', name='model_fields'),
    url(r'^(?P<dashboard_name>\w+)/$', 'curator.views.dashboard', name='dashboard_view'),
    url(r'^(?P<dashboard_name>\w+)/order/$', 'curator.views.widget_order', name='widget_order'),
)
