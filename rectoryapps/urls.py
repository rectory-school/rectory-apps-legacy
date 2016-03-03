from django.conf.urls import include, url
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView

from google_auth.views import LogonView

urlpatterns = [
    url(r'^admin/login/$', LogonView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
    url(r'^evaluations/', include('courseevaluations.urls')),
    url(r'^icons/', include('paw.urls')),
    url(r'^seating/', include('seating_charts.urls')),
    url(r'^calendar/', include('calendar_generator.urls')),
    url(r'^enrichment/', include('enrichmentmanager.urls')),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^google_auth/', include('google_auth.urls', namespace="google-auth")),
    url(r'^academics/', include('academics.urls', namespace="academics"))
]

if settings.DEBUG:
  urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)