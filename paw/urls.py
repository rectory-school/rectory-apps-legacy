from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^html/(?P<slug>[\w-]+)/$', 'paw.views.static', name='paw_static'),
    url(r'^json/page/(?P<slug>[\w-]+)/$', 'paw.views.json_from_page', name='paw_json_page'),
    url(r'^json/email/', 'paw.views.json_from_email', name='paw_json_email'),
    url(r'^json/default/$', 'paw.views.json_default', name='paw_json_default'),
)
