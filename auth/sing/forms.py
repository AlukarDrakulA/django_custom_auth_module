from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .utils import reply_email_code


# получаем модель User согласно настройкам settings.py
User = get_user_model()


class MyAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if not self.user_cache.verify_status:
                reply_email_code(self.user_cache)
                raise ValidationError('Email not verify! Check you email.', code='invalid_verify')
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.changed_data

# класс переопределения модели для приложения sing
class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email',
            'username',
            )


# форма для подтверждения аккаунта по коду
class ConfirmEmailCodeForm(forms.Form):
    entered_verify_code = forms.CharField(max_length = 6)
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

