from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'google_auth.views.login', name='login'),
)