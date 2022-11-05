import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


User = get_user_model()


# функция генерации кода подтвержения
def generate_verify_code():
    return random.randint(100000, 999999)


# активируем юзера если код верный, елси не верный пока принтим в консоль. Функционал неполный.
def activate_user(user_email, code):
    user_email = User.objects.get(email = user_email).email
    auth_code = User.objects.get(email = user_email).auth_code

    if user_email == user_email and auth_code == code:
        User.objects.filter(email = user_email).update(verify_status = True)
    else:
        print("Invalid verify code")


# проверяем статус пользователя
def get_user_verify_status(user_id):
    data = User.objects.get(pk = user_id)
    data_v = data.verify_status

    return data_v


def reply_email_code(user):
    username = User.objects.get(pk = user.id).username
    auth_code = User.objects.get(pk = user.id).auth_code
    email = User.objects.get(pk = user.id).email

    send_mail(
        subject=f'Game Portal. Confirm key.',
        message=f"Здравствуй, {username}!"
                f"Твой код подтверждения для завершения регистрации: {auth_code}\n"
                f"Страница для подтверждения email: http://127.0.0.1:8000/sing/confirm_email/",
        from_email='alastor91@mail.ru',
        recipient_list = [email]
        )