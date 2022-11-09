from django import forms
from .models import City, Language, Vacancy


class FindForm(forms.Form):
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={
                                      'class': 'form-control js-example-basic-single'}))
    language = forms.ModelChoiceField(label='Programming language', queryset=Language.objects.all(),
                                      to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={
                                          'class': 'form-control js-example-basic-single'}))


class VacancyViewForm(forms.ModelForm):
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control js-example-basic-single'}))
    language = forms.ModelChoiceField(label='Programming language', queryset=Language.objects.all(),
                                      widget=forms.Select(attrs={
                                          'class': 'form-control js-example-basic-single'}))
    url = forms.CharField(label='URL', widget=forms.URLInput(
        attrs={'class': 'form-control'}))
    title = forms.CharField(label='Job title', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    company = forms.CharField(label='Company', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(label='Job description',
                                  widget=forms.Textarea(
                                      attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = '__all__'
