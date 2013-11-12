# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect, Http404, HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .forms import UrlCreateForm
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

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'User registered and logged in with success.')
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            context = {'user_register_form': form}
    else:
        context = {'user_register_form': UserCreationForm()}
    return render(request, 'register.html', context)


def user_url_list(user, page):
    """
    Returns a paginator of a list of users Url's.
    """

    url_list = Url.objects.filter(user=user)
    paginator = Paginator(url_list, 20)
    try:
        url_list = paginator.page(page)
    except PageNotAnInteger:
        url_list = paginator.page(1)
    except EmptyPage:
        url_list = paginator.page(paginator.num_pages)
    return url_list


def index(request):
    """
    Main View, show form and list Url`s of the authenticated user.
    """

    if request.user.is_authenticated():
        context = {
            # Returns the users ``Url.objects`` QuerySet or None if Anonymous.
            'url_list': user_url_list(request.user, request.GET.get('page')),
            'absolute_uri': request.build_absolute_uri(),
            'user': request.user
        }
    else:
        context = {
            'user_login_form': AuthenticationForm(),
            'user_register_form': UserCreationForm()
        }

    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = (
                request.user if request.user.is_authenticated() else None
            )
            instance = form.save()
            context['short_url'] = request.build_absolute_uri() + instance.short_code
    else:
        form = UrlCreateForm()
    context['change_form'] = form

    return render(request, 'index.html', context)
