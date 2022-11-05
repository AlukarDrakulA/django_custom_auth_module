from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.views import LoginView

from sing.forms import MyUserCreationForm, ConfirmEmailCodeForm, MyAuthenticationForm
from .utils import activate_user, get_user_verify_status


User = get_user_model()


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': MyUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email = email, password = password)
            user_id = User.objects.get(email = email).id

            if get_user_verify_status(user_id) == True:
                login(request, user)
                return redirect('/')
            else:
                return redirect('confirm_email')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ConfirmEmail(View):
    template_name = 'registration/confirm_email.html'

    def get(self, request):
        context = {
            'form': ConfirmEmailCodeForm()
        }
        return render(request, self.template_name, context)


    def post(self, request):      
        form = ConfirmEmailCodeForm(request.POST)

        if form.is_valid():
            confirm_code = form.cleaned_data.get('entered_verify_code')
            user_email = form.cleaned_data.get('email')
            activate_user(user_email, confirm_code)
            return redirect('login')
        else:
            return redirect('confirm_email')
        
        




# username нам больше не нужен так как аутентифицируемся по почте
# username = form.cleaned_data.get('username')
# email = form.cleaned_data.get('email')
# password = form.cleaned_data.get('password1')

# user = authenticate(email = email, password = password)

# send_email_code_for_verify()

# return redirect('confirm_email')

# ! избавляемся от логина после регистрации, так как будем подтверждать по email
# login(request, user)