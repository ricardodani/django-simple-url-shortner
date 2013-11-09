from django import forms
from .models import Url
from .converter import num_to_base62

class UrlCreateForm(forms.ModelForm):

    class Meta:
        model = Url
        exclude = ['short_code']
