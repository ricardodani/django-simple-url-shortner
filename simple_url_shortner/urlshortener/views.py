from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .forms import UrlCreateForm
from .models import Url

@require_POST
def create(request):
    form = UrlCreateForm(request.POST)
    if form.is_valid():
        kwargs = {'url': form.cleaned_data['url']}
        custom = form.cleaned_data['custom']
        if custom:
            # specify an explicit id corresponding to the custom url
            kwargs.update({'id': base62.to_decimal(custom)})
        link = Link.objects.create(**kwargs)
        return render(request, 'shortener/submit_success.html', {'link': link})
    else:
        return render(request, 'shortener/submit_failed.html', {'link_form': form})

@require_GET
def index(request):
    """
    Main View, show form and list URL's of the authenticated user.
    """
    context = {
        'url_list': Url.objects.all(),
        'create_form': UrlCreatForm(),
    }
    return render(request, 'index.html', context)
