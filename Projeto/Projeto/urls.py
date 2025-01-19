"""
URL configuration for Projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Projeto import settings
from SAFERapp.views import HomeView, FormularioView, CadastroView, telaUsuario, logout_view, telaOcorrencias, telaPerfil, telaDetalhesChamado


# todas as URLs do projeto
urlpatterns = [
    path('admin/', admin.site.urls),
    # URL da página inicial
    path('', HomeView.as_view(), name='home'),
    # URL da página de formulario
    path('formulario/', FormularioView.as_view(), name='formulario'),
    # URL da página de cadastro
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    # URL da página de usuario
    path('Dashboard/<str:username>', telaUsuario, name ='telaUsuario'),
    #URL para deslogar o usuario
    path('logout/', logout_view, name='logout'),
    # URL da página de ocorrencias
    path('chamados/<str:tipoChamado>', telaOcorrencias, name ='telaChamados'),
    #URL da página de perfil
    path('meu-perfil/<str:username>', telaPerfil, name ='telaPerfil'),
    #URL da página de detalhamento de chamado
    path('chamado/<int:id>', telaDetalhesChamado, name ='telaDetalhesChamado'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)