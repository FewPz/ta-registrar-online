from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib import messages
import requests
from taauth.forms import AuthForm
from taauth.models import User
from os import getenv
from requests.exceptions import RequestException

# Create your views here.
class AuthLoginView(LoginView):
    authentication_form = AuthForm.LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        ldap_user = self.ldap_authenticate(username, password)
        if ldap_user:
            user, created = User.objects.get_or_create(username=username)

            if created:
                # Set the password and other user details from LDAP
                user.set_password(password)  # Hash password for security
                user.first_name = ldap_user.get('firstname')
                user.last_name = ldap_user.get('lastname')
                user.save()

            # Log the user in and redirect to the dashboard
            login(request, user)
            return redirect('dashboard')
        
        messages.error(request, 'Invalid credentials. Please try again.')
        return redirect('login')

    def ldap_authenticate(self, username, password):
        """Authenticate the user against an external LDAP server."""
        ldap_url = getenv('AUTH_ITKMITL_RESTAPI')
        try:
            response = requests.post(ldap_url, json={'username': username, 'password': password})
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except RequestException as e:
            messages.error(self.request, 'Error connecting to the external authentication service. Please try again later.')
            return None
