import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacaoStaffConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated and self.scope["user"].is_staff: # se o usuário está autenticado e é staff
            self.user = self.scope["user"]
            self.group_name = "staff_notificacoes" # Grupo Web Socke Global ( Trocar para algo mais único se precisar )

            # Adiciona o WebSocket ao grupo de notificações de staff
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            # Aceita a conexão WebSocket
            await self.accept()

            # DEBUG
            print(f"Usuário {str(self.user.nome)} conectado ao grupo {self.group_name}")

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated and self.scope["user"].is_staff:
            # Remove do grupo de notificações de staff ao desconectar
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receber_notificacao(self, event):
        mensagem = event["mensagem"]
        await self.send(text_data=json.dumps({"mensagem": mensagem}))

    async def receive(self, text_data): # esse metodo PRECISA estar aqui não remova
        pass