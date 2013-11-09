from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .forms import UrlCreateForm
from .models import Url

def index(request):
    """
    Main View, show form and list Url`s of the authenticated user.
    """
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # get short_url, set short_url in context
            # context['short_url'] = num_to_b62(request.POST.get('url')) # <- DRY Alert.
    else:
        form = UrlCreateForm()

    usr = request.user
    context = {
        # Returns the users ``Url.objects`` QuerySet or None if Anonymous.
        'url_list': Url.objects.filter(user=usr) if usr.is_authenticated() else None,
        # Form to insert url to shortener
        'create_form': form,
    }
    return render(request, 'index.html', context)
