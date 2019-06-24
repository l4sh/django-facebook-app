from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import logout


class LoginView(TemplateView):
    """Display login form to user"""
    template_name = "userauth/login.html"

class LogoutView(RedirectView):
    """Process logout"""
    url = '/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)