from django.shortcuts import render
from django.views import View
from .forms import AuthForm

# Create your views here.
class LoginView(View):
    
    def get(self, request):
        form = AuthForm.LoginForm()
        return render(request, 'login.html', {'form': form})