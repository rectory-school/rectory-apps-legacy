from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^html/(?P<slug>[\w-]+)/$', 'paw.views.static', name='paw_static'),
    url(r'^json/(?P<slug>[\w-]+)/$', 'paw.views.dynamic_data', name='paw_json'),
)
