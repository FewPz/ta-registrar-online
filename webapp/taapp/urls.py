from django.urls import path
from taapp.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login')
]
