import os

from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('',
    #(r'^$', 'home', name='dashboard'),
    (r'^widget/(?P<widget_id>\d+)/$', 'dashboard.views.widget'),
)
