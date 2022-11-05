from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email_addres'), unique = True)
    verify_status = models.BooleanField(default=False)
    auth_code = models.CharField(max_length = 6)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        ]
    