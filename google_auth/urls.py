from django.conf.urls import patterns, include, url

from google_auth import views

urlpatterns = patterns('',
    url(r'^login/$', views.LogonView.as_view(), name='login'),
)