from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from scraping.models import City, Language


User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the email',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the password',
    }))

    def clean(self, *args, **kwargs):
        '''
        qs[0] - to take first element
        .password = take the password of first element
        '''
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()
        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise ValidationError('There is no such user')
            if not check_password(password, qs[0].password):
                raise ValidationError("Invalid password")
            user = authenticate(email=email, password=password)
            if not user:
                raise ValidationError("The user's account is disabled")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the email',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the password',
    }))
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm the password',
    }))

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise ValidationError("Passwords did not match")
        return data['password2']

    class Meta:
        model = User
        fields = ('email', )


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                                  to_field_name='slug', required=True,
                                  widget=forms.Select(attrs={
                                      'class': 'form-control js-example-basic-single'}))
    language = forms.ModelChoiceField(label='Programming language', queryset=Language.objects.all(),
                                      to_field_name='slug', required=True,
                                      widget=forms.Select(attrs={
                                          'class': 'form-control js-example-basic-single'}))
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='Subscribe to the mailing?')

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email', )


class ContactForm(forms.Form):
    city = forms.CharField(label='City',
                           required=True,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Enter the city',
                           }))
    language = forms.CharField(label='Programming language',
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Enter the programming language',
                               }))
    email = forms.CharField(label='Email', required=True,
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Enter the email',
                            }))

