from django.urls import path
from taapp.views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
