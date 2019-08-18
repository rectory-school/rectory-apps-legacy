
""" URLS for the paw """

from django.urls import path

from paw import views

app_name = 'paw'

urlpatterns = [
    path('html/(?P<slug>[\w-]+)/$', views.static, name='paw_static'),
    path('json/page/(?P<slug>[\w-]+)/$', views.json_from_page, name='paw_json_page'),
    path('json/email/', views.json_from_email, name='paw_json_email'),
    path('json/default/$', views.json_default, name='paw_json_default'),
]
