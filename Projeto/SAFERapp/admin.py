from django.contrib import admin
from .models import CustomUser
from SAFERapp.beans.Post import Post
from SAFERapp.beans.Ocorrencia import Ocorrencia
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Ocorrencia)