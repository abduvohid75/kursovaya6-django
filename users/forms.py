from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User
from main.forms import StyleForm

class UserRegisterForm(StyleForm, UserCreationForm):

    class Meta:
        model = User
        fields = ('avatar', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UserProfileForm(StyleForm, UserChangeForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

