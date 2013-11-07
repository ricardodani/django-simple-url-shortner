from django import forms
from .converter import num_to_base62
from .models import Url

class UrlCreateForm(forms.ModelForm):

    class Meta:
        model = Url
        exclude = ['user', 'short_code']
