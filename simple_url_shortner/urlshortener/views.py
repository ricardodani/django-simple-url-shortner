# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect, Http404
from django.views.decorators.http import require_GET

from .forms import UrlCreateForm
from .models import Url


@require_GET
def redirect(request, short_code):
    if short_code:
        try:
            url = Url.objects.get(short_code=short_code)
        except Url.DoesNotExists:
            raise Http404()
    return HttpResponsePermanentRedirect(url)

def index(request):
    """
    Main View, show form and list Url`s of the authenticated user.
    """
    context = {
        'url_list': (
            # Returns the users ``Url.objects`` QuerySet or None if Anonymous.
            Url.objects.filter(user=request.user)
            if request.user.is_authenticated()
            else None
        ),
        'user': request.user
    }

    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            instance = form.save()
            context['short_url'] = instance.get_absolute_url()
    else:
        form = UrlCreateForm()

    context['change_form'] = form
    return render(request, 'index.html', context)
