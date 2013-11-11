from django import forms
from django.contrib.auth import forms as auth_forms
from .models import Url
from .converter import num_to_base62

class UserRegisterForm(auth_forms.UserCreationForm):
    pass


class UserLoginForm(auth_forms.AuthenticationForm):
    pass


class UrlCreateForm(forms.ModelForm):

    class Meta:
        model = Url
        exclude = ['short_code']
