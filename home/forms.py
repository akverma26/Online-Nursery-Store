from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import Account, Plant, PlantImage


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email address'
        self.fields['username'].widget.attrs['placeholder'] = 'Create a Username'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter your Name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Choose a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

    class Meta:
        model = Account
        fields = ('email', 'username', 'name')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'


class AddPlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddPlantForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Plant Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Plant Description'
        self.fields['price'].widget.attrs['placeholder'] = 'Enter Plant Price'

    class Meta:
        model = Plant
        fields = ('name', 'description', 'price')


class AddPlantImageForm(forms.ModelForm):

    class Meta:
        model = PlantImage
        fields = ('image',)
