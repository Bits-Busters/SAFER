from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from SAFERapp.models import CustomUser
from SAFERapp.beans.Ocorrencia import Ocorrencia 
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=CustomUser)
def enviar_email_boas_vindas(sender, instance, created, **kwargs):
    if created:  # Só envia o email quando o usuário for criado
        subject = 'Bem-vindo ao nosso site!'
        message = f'Olá {instance.nome}, obrigado por se cadastrar no nosso site!'
        from_email = settings.DEFAULT_FROM_EMAIL  # Usando o valor configurado no settings.py
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)



@receiver(post_save, sender=Ocorrencia)
def envia_email_status_alterado(sender, instance, **kwargs):
    if instance.pk: # verifica se já existe no banco (meio redudante)
        subject = 'Status da Ocorrência!' # Titulo do email
        message = f'Olá {instance.Nome_Autor}, status da ocorrência do animal {instance.Nome_Animal} foi alterado para {instance.Status}!' # Corpo do email
        from_email = settings.DEFAULT_FROM_EMAIL  # Usando o valor configurado no settings.py
        recipient_list = [instance.Autor.email] # Lista de destinatários
        send_mail(subject, message, from_email, recipient_list) # Envia o email



customuser = get_user_model() #pega o modelo de AUTH_USER_MODEL 
@receiver(post_save, sender=Ocorrencia)
def notifica_novo_chamado(sender, instance, created, **kwargs):
    if created:
        lista_staff = CustomUser.objects.filter(is_staff=True)
        channel_layer = get_channel_layer()  # Instância do layer do Channels
        mensagem = f"Um novo chamado foi criado"
        for staff_instance in lista_staff:
            # Envia a notificação em tempo real para o WebSocket do staff
            async_to_sync(channel_layer.group_send)(
                f"staff_notificacoes", # Esse é o nome do grupo (o mesmo do group_name de consumers.py)
                {
                    "type": "receber_notificacao",
                    "mensagem": mensagem  # Mensagem para o WebSocket
                }
            )