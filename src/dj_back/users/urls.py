from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm), name='login')
]
