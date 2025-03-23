from django.urls import re_path
from .consumers import NotificacaoStaffConsumer

websocket_urlpatterns = [
    re_path(r'ws/staff/notificacoes/$', NotificacaoStaffConsumer.as_asgi()),
]