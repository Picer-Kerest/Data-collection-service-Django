from django import forms
from .models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={
                                      'class': 'form-control js-example-basic-single'}))
    language = forms.ModelChoiceField(label='Programming language', queryset=Language.objects.all(),
                                      to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={
                                          'class': 'form-control js-example-basic-single'}))

