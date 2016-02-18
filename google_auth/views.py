from django.shortcuts import render, redirect
from django.conf import settings

from django.utils.http import is_safe_url

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from django.http import JsonResponse

from django.views.generic import View

from django.contrib.auth.models import Group

from enrichmentmanager.models import Teacher

import requests

class LogonView(View):
    def get(self, request):
        return self.login_page(request)
    
    def post(self, request):
        logon_type = request.POST.get("logon_type")
        
        if logon_type == "native":
            return self.handle_django_logon(request)
        elif logon_type == "google":
            return self.handle_google_logon(request)
    
    def set_groups(self, user):
        try:
            group = Group.objects.get(name="Advisors")
        except Group.DoesNotExist:
            group = None
        
        try:
            advisor = Teacher.objects.get(academic_teacher__email=user.email)

        except Teacher.DoesNotExist:
            user.groups.remove(group)
            user.save()
            
            return
        
        if advisor.academic_teacher.active:
            user.groups.add(group)
            user.save()

        else:
            user.groups.remove(group)
            user.save()
    
    def handle_google_logon(self, request):
        id_token = request.POST.get("id_token")
        
        if not id_token:
            raise ValueError()
        
        payload = {'id_token': id_token}
            
        r = requests.get("https://www.googleapis.com/oauth2/v3/tokeninfo", params=payload)
        
        data = r.json()
        
        email = data["email"]
        last_name = data["family_name"]
        first_name = data["given_name"]
        hosted_domain = data.get("hd", "")
                
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
        
        self.set_groups(user)
            
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
            
            self.set_groups(user)
            
            # Bring them to where they really want to go
            return redirect(redirect_to)
        else:
            # Password was wrong or something, bring us back to the login page
            
            return self.login_page(request, processed_form=form, start_with_django_dialog=True)
