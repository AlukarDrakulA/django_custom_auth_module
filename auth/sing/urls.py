from django.urls import path, include
from django.views.generic import TemplateView

from sing.views import Register, ConfirmEmail, MyLoginView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name = 'login'),

    path('', include('django.contrib.auth.urls')), # по сути страниц для логина лежит тут, поэтому нет отдельной view

    path('confirm_email/', ConfirmEmail.as_view(), name='confirm_email'), # url стрницы с формопй подтверждения емела по коду

    path('register/', Register.as_view(), name='register'), # регистрация
]