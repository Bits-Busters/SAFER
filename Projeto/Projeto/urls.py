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

from SAFERapp.views import HomeView, FormularioView, CadastroView, telaUsuario, logout_view, telaOcorrencias, telaPerfil, TelaDetalhesChamadoView, InformativosView, GerenciarInformativosView, CriarInformativoView, TelaCriarObservacoesView, notificacoes_view, notificacao_lida
from django.contrib.auth import views as auth_views


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
    path('meu-perfil/<str:username>', PerfilView.as_view(), name ='telaPerfil'),
    #URL da página de detalhamento de chamado
    path('chamado/<int:id>',TelaDetalhesChamadoView.as_view(), name ='telaDetalhesChamado'),
    # URL da página de atualização de chamado
    path('chamado/<int:ocorrencia_id>/atualizar', AtualizarOcorrenciaView.as_view(), name='telaAtualizarChamado'),

    #URL da página de Informativos
    path('informativos/', InformativosView.as_view(), name ='telaInformativos'),
    #URL da página de atualização de Informativos
    path('informativos/criar/<int:id>', CriarInformativoView.as_view(), name ='criarInformativo'),
    #URL da página de criação de Informativos
    path('informativos/criar/', CriarInformativoView.as_view(), name ='criarInformativoNovo'),
    #URL da página de gerenciamento de Informativos
    path('informativos/gerenciar/', GerenciarInformativosView.as_view(), name ='gerenciarInformativos'),
    
    # Noticicações
    path('staff/notificacoes', notificacoes_view, name="staffNotificacoes" ),
    path('staff/notificacaolida', notificacao_lida, name='notificacaolida'),


    # Página para reiniciar a senha
    path('senha-reset/', auth_views.PasswordResetView.as_view(template_name='reset_password_templates/password_reset_form.html'), name='password_reset'),
    # Página de notificação de sucesso após o envio do email
    path('senha-reset-feito/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_templates/password_reset_done.html'), name='password_reset_done'),
    # Página de redefinição de senha com o token (enviado por email)
    path('redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_templates/password_reset_confirm.html'), name='password_reset_confirm'),
    # Sucesso após redefinição da senha
    path('senha-reset-completa/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_templates/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


