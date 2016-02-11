from django.shortcuts import render
from django.conf import settings

def login(request):
    context = {
        'google_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'google_hosted_domain': settings.GOOGLE_HOSTED_DOMAIN
    }
    
    return render(request, "google_auth/login.html", context)