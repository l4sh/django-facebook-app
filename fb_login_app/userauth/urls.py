from django.conf import settings
from django.urls import path
from . import views

app_name = 'userauth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('facebook/deauth/', views.FacebookDeauthView.as_view(), name='deauth'),
]