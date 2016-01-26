from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rectory_paw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^text/(?P<slug>[\w-]+)/$', 'paw.views.text', name='paw_text'),
    url(r'^html/(?P<slug>[\w-]+)/$', 'paw.views.static', name='paw_static'),
    url(r'^json/(?P<slug>[\w-]+)/$', 'paw.views.dynamic_data', name='paw_json'),
)
