from django.conf.urls.defaults import *
from django.conf import settings

from .views import timeline_detail_json

urlpatterns = patterns('',
    url(
        regex   = '^(?P<pk>[-\w]+)/json/$',
        view    = timeline_detail_json,
        kwargs  = {},
        name    = 'timeline_detail_json',
    ),
)

'''
TODO: add urls attached to basic list/detail views
'''