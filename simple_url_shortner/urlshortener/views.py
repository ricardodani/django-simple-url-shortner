from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import AbstractBaseUser
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from .forms import UrlCreateForm
from .models import Url


@cache_page(60 * 60)
@require_GET
def redirect(request: HttpRequest, short_code: str) -> HttpResponsePermanentRedirect:
    """Redirect to the original URL associated with a short code."""
    try:
        url = Url.objects.get(short_code=short_code)
    except Url.DoesNotExist as exc:
        raise Http404 from exc
    return HttpResponsePermanentRedirect(url.original_url)


def register_user(request: HttpRequest) -> HttpResponse:
    form: UserCreationForm
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            if user is None:
                raise RuntimeError("The newly created user could not be authenticated.")
            login(request, user)
            messages.success(request, "Account created successfully.")
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"user_register_form": form})


def user_url_list(
    user: AbstractBaseUser, page: str | None, limit: int = 20
) -> Page[Url]:
    paginator = Paginator(Url.objects.filter(user_id=user.pk), limit)
    try:
        return paginator.page(page if page is not None else 1)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        context: dict[str, Any] = {
            "url_list": user_url_list(request.user, request.GET.get("page")),
            "absolute_uri": request.build_absolute_uri("/"),
            "user": request.user,
        }
    else:
        context = {
            "user_login_form": AuthenticationForm(),
            "user_register_form": UserCreationForm(),
        }

    form: UrlCreateForm
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user if request.user.is_authenticated else None
            instance = form.save()
            context["short_url"] = request.build_absolute_uri("/") + instance.short_code
    else:
        form = UrlCreateForm()
    context["change_form"] = form

    return render(request, "index.html", context)
