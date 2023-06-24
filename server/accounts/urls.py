from django.urls import path
from django.contrib.auth import views
from accounts.views import register, profile


urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
]
