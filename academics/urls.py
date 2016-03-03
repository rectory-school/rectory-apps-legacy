from django.conf.urls import include, url
from academics.views import get_vcards

urlpatterns = [
    url(r'^familydata/family_vcard_data.vcf$', get_vcards, name="family_vcard_data"),
    ]
