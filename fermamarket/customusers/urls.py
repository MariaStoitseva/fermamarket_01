from django.urls import path
from .forms import CustomLoginForm
from .views import register_view, custom_logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', custom_logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm), name='login'),
]
