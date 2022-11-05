from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from sing.models import User
from sing.utils import generate_verify_code


# получаем модель User согласно настройкам settings.py
User = get_user_model()


@receiver(post_save, sender=User)
def verify_email(sender, instance, created, **kwargs):
    if created:
        auth_code = generate_verify_code()
        User.objects.filter(pk = instance.id).update(auth_code = auth_code)

        send_mail(
                subject=f'Game Portal. Confirm key.',
                message=f"Здравствуй, {instance.username}!"
                        f"Твой код подтверждения для завершения регистрации: {auth_code}\n"
                        f"Страница для подтверждения email: http://127.0.0.1:8000/sing/confirm_email/",
                from_email='alastor91@mail.ru',
                recipient_list = [instance.email]
                )
