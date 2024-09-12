from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):

    def get_success_url(self):
        # Check if there is a next parameter in the request, if so, redirect to it
        return self.get_redirect_url() or '/home'
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-primary focus:border-primary'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-primary focus:border-primary'
        })
    )
