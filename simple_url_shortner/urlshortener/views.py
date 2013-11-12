# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect, Http404
from django.views.decorators.http import require_GET, require_POST

from .forms import UrlCreateForm, UserRegisterForm, UserLoginForm
from .models import Url


@require_GET
def redirect(request, short_code):
    """
    Redirects Url
    """
    if short_code:
        try:
            url = Url.objects.get(short_code=short_code)
        except Url.DoesNotExist:
            raise Http404()
    return HttpResponsePermanentRedirect(url.original_url)

@require_POST
def register_user(request):
    return render(request, 'register.html')


def index(request):
    """
    Main View, show form and list Url`s of the authenticated user.
    """
    if request.user.is_authenticated():
        context = {
            # Returns the users ``Url.objects`` QuerySet or None if Anonymous.
            'url_list': Url.objects.filter(user=request.user),
            'user': request.user
        }
    else:
        context = {
            'user_login_form': UserLoginForm(),
            'user_register_form': UserRegisterForm()
        }

    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = (
                request.user if request.user.is_authenticated() else None
            )
            instance = form.save()
            context['short_url'] = instance.get_absolute_url()
    else:
        form = UrlCreateForm()
    context['change_form'] = form

    return render(request, 'index.html', context)
