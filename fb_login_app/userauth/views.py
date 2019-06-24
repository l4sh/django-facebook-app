from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from social_django.models import UserSocialAuth


class LoginView(TemplateView):
    """Display login form to user"""
    template_name = "userauth/login.html"

class LogoutView(RedirectView):
    """Process logout"""
    url = '/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='get')
class ProfileView(TemplateView):
    """Display the user profile"""
    template_name = 'userauth/profile.html'

    def get(self, *args, **kwargs):
        # Add facebook user id and avatar to user object
        params = {'user': self.request.user, 'provider': 'facebook'}
        fb_profile = get_object_or_404(UserSocialAuth, **params)
        self.request.user.facebook_uid = fb_profile.uid
        fb_avatar = 'https://graph.facebook.com/{}/picture?type=large'.format(fb_profile.uid)
        self.request.user.facebook_avatar = fb_avatar
        return super(ProfileView, self).get(*args, **kwargs)