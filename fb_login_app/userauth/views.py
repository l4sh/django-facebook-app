from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, RedirectView, View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from social_django.models import UserSocialAuth
from social_core.backends.facebook import FacebookOAuth2
from .utils import load_signed_request


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


@method_decorator(csrf_exempt, name='dispatch')
class FacebookDeauthView(View):
    """Handle the facebook deauthorization callback"""

    def post(get, request, *args, **kwargs):
        signed_request = request.POST.get('signed_request')
        if not signed_request:
            return HttpResponse('No signed request present', status=400)

        # Handle signed request with social_core
        FacebookOAuth2.load_signed_request = load_signed_request
        fb = FacebookOAuth2()
        parsed_signed_request = fb.load_signed_request(signed_request)

        try:
            params = {'uid': parsed_signed_request.get('user_id'),
                      'provider': 'facebook'}
            social_user = get_object_or_404(UserSocialAuth, **params)
            user = social_user.user
            # Deauth request is successful
            user.is_active = False
            user.save()
            return HttpResponse('Deauthorization successful', status=200)
        except:
            # Deauth request fails
            return HttpResponse('Error deauthorizing application', status=400)
