import re

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        LOGIN_EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
        LOGIN_EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URL]
        path = request.path_info.lstrip('/')
        login_exempt_url = any(url.match(path) for url in LOGIN_EXEMPT_URLS)

        if path == '':
            return None
        if request.user.is_authenticated and login_exempt_url:
            return redirect(reverse('dashboard'))
        elif request.user.is_authenticated or login_exempt_url:
            return None
        else:
            return redirect(reverse('login'))


class AdminOnlyPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.user.groups:
            request.user_group = request.user.groups.all()[0].name
        print(request.user.groups)
        pass
