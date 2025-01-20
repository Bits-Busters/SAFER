from django.apps import AppConfig


class SaferappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SAFERapp'

    def ready(self):
        import SAFERapp.signals # importa os signals