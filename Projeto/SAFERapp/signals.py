from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from SAFERapp.models import CustomUser  # Ajuste conforme o nome do seu app

@receiver(post_save, sender=CustomUser)
def enviar_email_boas_vindas(sender, instance, created, **kwargs):
    if created:  # Só envia o email quando o usuário for criado
        subject = 'Bem-vindo ao nosso site!'
        message = f'Olá {instance.nome}, obrigado por se cadastrar no nosso site!'
        from_email = settings.DEFAULT_FROM_EMAIL  # Usando o valor configurado no settings.py
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)