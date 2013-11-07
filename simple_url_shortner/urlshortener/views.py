from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .forms import UrlCreateForm
from .models import Url

def index(request):
    """
    Main View, show form and list URL's of the authenticated user.
    """
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # message.success with URL ?
            # redirect to GET home
    else:
        form = UrlCreateForm()

    context = {
        'url_list': Url.objects.all(),
        'create_form': form,
    }
    return render(request, 'index.html', context)
