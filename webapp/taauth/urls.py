from django.urls import path, include
from taauth.views import AuthLoginView

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("login/", AuthLoginView.as_view(), name="login"),
]
