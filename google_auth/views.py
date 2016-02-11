from django.shortcuts import render, redirect
from django.conf import settings

from django.utils.http import is_safe_url

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

from django.views.generic import View

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
    
    def login_page(self, request, processed_form=None, start_with_django_dialog=False):
        context = {
            'google_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'google_hosted_domain': settings.GOOGLE_HOSTED_DOMAIN,
            'start_django_form': start_with_django_dialog,
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
