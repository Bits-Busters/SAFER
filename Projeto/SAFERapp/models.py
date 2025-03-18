from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from SAFERapp.beans.Enums import RelacaoUFRPE, TipoUsuario

from django.conf import settings

# Manager para o Custom User
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("O email deve ser fornecido")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # Definir valores padrão para campos de usuário normal
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        # Definir valores padrão para campos de superusuário
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# Modelo Customizado
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Removendo o campo `username` padrão, usando email como identificador
    username = None
    email = models.EmailField(unique=True, primary_key=True, verbose_name="Email")

    # Campos extras
    nome = models.CharField(max_length=100, verbose_name="Nome")
    telefone = models.CharField(max_length=15, blank=False, verbose_name="Telefone")
    telefone_fixo = models.CharField(max_length=15, blank=True, verbose_name="Telefone Fixo")
    relacao_ufrpe = models.CharField(
        max_length=20,
        choices=RelacaoUFRPE.choices,
        default=RelacaoUFRPE.VISITANTE,
        verbose_name="Relação com a UFRPE",
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.COMUM,
        verbose_name="Tipo de Usuário",
    )

    # Campos necessários para autenticação
    is_active = models.BooleanField(default=True)  # Campo para verificar se o usuário está ativo
    is_staff = models.BooleanField(default=False)  # Campo para verificar se o usuário é staff
    is_superuser = models.BooleanField(default=False)  # Campo para verificar se o usuário é superusuário

    # Sobrescrevendo o manager padrão
    objects = CustomUserManager()

    # Definindo o campo usado para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'tipo_usuario']

    def __str__(self):
        return f"{self.nome} ({self.tipo_usuario})"

    # Métodos personalizados
    def atualizar_informacoes(self, **kwargs):
        """
        Atualiza as informações pessoais do usuário.
        """
        for campo, valor in kwargs.items():
            if hasattr(self, campo):  # Verifica se o campo existe no modelo
                setattr(self, campo, valor)
            else:
                raise AttributeError(f"O campo '{campo}' não existe no modelo.")
        self.save()

    def promover_usuario(self, novo_tipo: TipoUsuario):
        """
        Promove o tipo de usuário para um novo tipo, verificando se o tipo é válido.
        """
        if novo_tipo not in TipoUsuario.choices:
            raise ValueError(f"Tipo de usuário '{novo_tipo}' não é válido.")
        self.tipo_usuario = novo_tipo
        self.save()

    def registrar_ocorrencia(self, descricao, local, imagens, registro):
        """
        Registra uma ocorrência com as informações fornecidas.
        """
        # Aqui você pode interagir com um modelo real de Ocorrência, se houver
        return f"Ocorrência registrada: {descricao} no local {local} com registro {registro}."

def get_or_create_anonymous_user():
        try:
            return CustomUser.objects.get(nome='Anônimo Usuário')
        except CustomUser.DoesNotExist:
            return CustomUser.objects.create(
                email='anonimo@example.com',
                nome="Anônimo Usuário",
                telefone="000000000",
                telefone_fixo="000000000",
                relacao_ufrpe="VISITANTE",
                tipo_usuario="COMUM",
                is_active=True
            )

from SAFERapp.beans.Ocorrencia import Ocorrencia 
class Notificacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, null=True, blank=True)
    mensagem = models.CharField(max_length=255)
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario} - {self.mensagem}"
    
class PasswordHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_history')
    password_hash = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Senha de {self.user.username} - {self.changed_at}"

    class Meta:
        ordering = ['-changed_at']