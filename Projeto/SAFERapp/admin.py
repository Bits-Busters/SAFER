from django.contrib import admin
from .models import CustomUser
from SAFERapp.beans.Informativos import Informativo
from SAFERapp.beans.Ocorrencia import Ocorrencia
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Informativo)
admin.site.register(Ocorrencia)