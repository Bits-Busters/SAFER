from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from Enums import RelacaoUFRPE, TipoUsuario

# Manager para o Custom User
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser fornecido")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Modelo Customizado
class CustomUser(AbstractUser):
    # Removendo o campo `username` padrão, usando email como identificador
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

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
            if hasattr(self, campo):
                setattr(self, campo, valor)
        self.save()

    def promover_usuario(self, novo_tipo: TipoUsuario):
        """
        Promove o tipo de usuário.
        """
        self.tipo_usuario = novo_tipo
        self.save()

    def realizar_ocorrencia(self, descricao, local, imagens, registro):
        """
        Simula a criação de uma ocorrência.
        """
        return f"Ocorrência registrada: {descricao} no local {local} com registro {registro}."
