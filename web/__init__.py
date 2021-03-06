from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

default_app_config = 'web.apps.WalletConfig'


class ClientRedirectResponse(JsonResponse):
    def __init__(self, redirect_url, replace=False, **kwargs):
        super().__init__(data={'redirect_url': redirect_url, 'replace': replace}, **kwargs)


def custom_uri(view, **kwargs):
    return '{}?{}'.format(reverse(view), urlencode(kwargs))


def server_redirect(view, **kwargs):
    return redirect(custom_uri(view=view, **kwargs))


def client_redirect(view, replace=False, **kwargs):
    return ClientRedirectResponse(redirect_url=custom_uri(view=view, **kwargs), replace=replace)


def paginate(obj_list, page, per_page):
    return Paginator(obj_list, per_page=per_page).page(page)
