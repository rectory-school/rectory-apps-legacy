from django.shortcuts import render, redirect
from django.conf import settings

from django.utils.http import is_safe_url

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from django.http import JsonResponse

from django.views.generic import View

from apiclient import discovery
import httplib2
from oauth2client import client


class LogonView(View):
    def get(self, request):
        return self.login_page(request)
    
    def post(self, request):
        logon_type = request.POST.get("logon_type")
        
        if logon_type == "native":
            return self.handle_django_logon(request)
        elif logon_type == "google":
            return self.handle_google_logon(request)
    
    def handle_google_logon(self, request):
        print (request.POST)
        
        auth_code = request.POST.get("code")
        
        if not auth_code:
            raise ValueError()
            
        #TODO: Move to settings
        CLIENT_SECRET_FILE = '/Users/adam.peacock/development/rectoryapps/client_secret_file.json'
        
        credentials = client.credentials_from_clientsecrets_and_code(CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)
        
        email = credentials.id_token['email']
        hosted_domain = credentials.id_token.get('hd', "")
        
        desired_hosted_domain = settings.GOOGLE_HOSTED_DOMAIN
        
        if desired_hosted_domain and hosted_domain.lower() != desired_hosted_domain.lower():
            raise ValueError()
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            user.save()
        
        #We'll see if this works...
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        
        auth_login(request, user)
            
        return JsonResponse({'status_code': 200, 'email': email})
            
            
    def login_page(self, request, processed_form=None, start_with_django_dialog=False):
        context = {
            'google_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'google_hosted_domain': settings.GOOGLE_HOSTED_DOMAIN,
            'start_django_form': start_with_django_dialog,
            'next': request.GET.get('next', request.path)
        }
        
        if processed_form:
            context['django_auth_form'] = processed_form
        else:
            context['django_auth_form'] = AuthenticationForm(request)
            
        return render(request, "google_auth/login.html", context)
        
    def handle_django_logon(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        # Form does user authentication, so if it is valid we can proceed that the user entered
        # their credentials successfully
        if form.is_valid():
            redirect_to = request.GET.get("next", "/")
            
            # Log the user in
            auth_login(request, form.get_user())
            
            # Bring them to where they really want to go
            return redirect(redirect_to)
        else:
            # Password was wrong or something, bring us back to the login page
            
            return self.login_page(request, processed_form=form, start_with_django_dialog=True)
