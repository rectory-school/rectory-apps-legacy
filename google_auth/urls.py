from django.urls import path

from google_auth import views

app_name = 'google_auth'

urlpatterns = [
    path('login/', views.LogonView.as_view(), name='login'),
]