from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from SAFERapp.beans.Enums import StatusChamado
from SAFERapp.beans.Forms import FormularioForm, FilterForm, ImagemFormSet
from SAFERapp.beans.Forms import CadastroForm, InformativoForm, ObservacaoForm
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.beans.Informativos import Informativo
from SAFERapp.beans.Observacoes import Observacoes
from SAFERapp.models import Notificacao
from .models import CustomUser, get_or_create_anonymous_user

from SAFERapp.beans.Imagens import Imagens


# Create your views here.

@login_required
def telaOcorrencias(request, tipoChamado):
    if tipoChamado == "meus-chamados":
        # Obtém as ocorrências do usuário logado
        nome = "Meus chamados"
        ocorrencia = Ocorrencia.objects.filter(Autor=request.user).order_by('-DataHora')
    elif tipoChamado == "todos-os-chamados":
        # Obtém as ocorrências do usuário logado
        nome = "Todos os chamados"
        ocorrencia = Ocorrencia.objects.order_by('-DataHora')
    elif tipoChamado == "chamados-aceitos":
        # Obtém as ocorrências do usuário logado
        nome = "Chamados aceitos"
        ocorrencia = Ocorrencia.objects.filter(Resgatista=request.user).order_by('-DataHora')
    elif tipoChamado == "chamados-em-aberto":
        # Obtém as ocorrências do usuário logado
        nome = "Chamados em aberto"
        ocorrencia = Ocorrencia.objects.filter(Status=StatusChamado.ABERTO).order_by('-DataHora')
    else:
        messages.error(request, "Esta não é uma página válida")
        return render(request, 'home.html')
    form = FilterForm(request.GET or None)

    if form.is_valid():
        # Acessando os dados validados do formulário
        animal = form.cleaned_data.get('Animal')
        if animal:
            ocorrencia = ocorrencia.filter(Nome_Animal=animal)

        tipoCaso = form.cleaned_data.get('TipoCaso')
        if tipoCaso:
            ocorrencia = ocorrencia.filter(TipoCaso=tipoCaso)

        data = form.cleaned_data.get('Data')  # Aqui você acessa a data corretamente
        if data:
            ocorrencia = ocorrencia.filter(DataHora__date=data)  # Filtra apenas pela data, não pelo horário

        local = form.cleaned_data.get('Local')
        if local:
            ocorrencia = ocorrencia.filter(Local=local)

    # Cria um objeto Paginator para dividir as ocorrências em páginas com 5 itens cada
    paginator = Paginator(ocorrencia, 5)  # 5 ocorrências por página

    # Obtém o número da página atual
    page_number = request.GET.get('page')  # Pode vir da URL (por exemplo: ?page=2)
    page_obj = paginator.get_page(page_number)

    # Renderiza a página com as ocorrências paginadas
    return render(request, 'TelaChamados.html', {'page_obj': page_obj, 'form': form, 'nome': nome, 'filtro':tipoChamado})

def telaUsuario(request, username):
    if username != request.user.nome:
        messages.error(request, "Este não era o seu perfil")
        return render(request, 'home.html')
    return render(request, 'TelaUsuario.html')

class TelaDetalhesChamadoView(View):
    resgatistas = ['admin', 'gestor', 'analista']

    def get(self, request, id):
        ocorrencia = get_object_or_404(Ocorrencia, id=id)
        ocorrenciaImagem = Imagens.objects.filter(IdOcorrencia=ocorrencia).first()
        observacoes_ocorrencia = Observacoes.objects.filter(ocorrencia=ocorrencia).order_by('-dataHora')
        form = ObservacaoForm()  # Formulário de observação vazio
        
        return render(request, 'TelaDetalhesChamado.html', {
            "ocorrencia": ocorrencia, 
            "imagem": ocorrenciaImagem,
            "resgatistas": self.resgatistas,
            "observacoes": observacoes_ocorrencia,
            "form": form
        })

    def post(self, request, id):
        form_type = request.POST.get("form_type")  # Identifica a ação no formulário
        ocorrencia = get_object_or_404(Ocorrencia, id=id)

        if form_type == "aceitar_chamado":
            ocorrencia.Resgatista = request.user
            ocorrencia.Status = StatusChamado.EM_ANALISE
            ocorrencia.save()
            return redirect('home')

        elif form_type == "adicionar_observacao":
            form = ObservacaoForm(request.POST)
            if form.is_valid():
                observacao = form.save(commit=False)
                observacao.ocorrencia = ocorrencia
                observacao.autor = request.user
                observacao.save()
                messages.success(request, "Observação criada com sucesso!")
            else:
                messages.error(request, "Erro ao salvar a observação. Verifique os dados.")

        elif form_type == "editar_observacao":
            observacao_id = request.POST.get("observacao_id")
            observacao = get_object_or_404(Observacoes, id=observacao_id, ocorrencia=ocorrencia)

            if observacao.autor == request.user:  # Garante que o usuário só edite suas próprias observações
                form = ObservacaoForm(request.POST, instance=observacao)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Observação atualizada com sucesso!")
                else:
                    messages.error(request, "Erro ao atualizar a observação. Verifique os dados.")

        elif form_type == "excluir_observacao":
            observacao_id = request.POST.get("observacao_id")
            observacao = get_object_or_404(Observacoes, id=observacao_id, ocorrencia=ocorrencia)

            if observacao.autor == request.user:  # Garante que o usuário só exclua suas próprias observações
                observacao.delete()
                messages.success(request, "Observação excluída com sucesso!")

        form = ObservacaoForm()  # Formulário de observação vazio

        return redirect('telaDetalhesChamado', ocorrencia.id)


# Inicio da implementacao da tela de observacoes
class TelaCriarObservacoesView(View):
    def get(self, request, ocorrencia_id):
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        form = ObservacaoForm()
        return render(request, 'TelaObservacoes.html', {'form': form, 'ocorrencia': ocorrencia})

    def post(self, request, ocorrencia_id):
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        form = ObservacaoForm(request.POST)
        if form.is_valid():
            observacao = form.save(commit=False)
            observacao.ocorrencia = ocorrencia
            observacao.autor = request.user
            observacao.save()
            messages.success(request, "Observação criada com sucesso!")
            return redirect('telaDetalhesChamado', ocorrencia_id=ocorrencia.id)

        return render(request, 'TelaObservacoes.html', {'form': form, 'ocorrencia': ocorrencia})

class AtualizarOcorrenciaView(LoginRequiredMixin, View):
    resgatistas = ['admin', 'gestor', 'analista']

    def get(self, request, ocorrencia_id):
        """ Exibe o formulário preenchido com os dados da ocorrência """
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        form = FormularioForm(instance=ocorrencia)
        return render(request, 'TelaAtualizarDetalhesChamado.html', {'form': form, 'ocorrencia': ocorrencia, 'resgatistas': self.resgatistas})

    def post(self, request, ocorrencia_id):
        """ Processa a atualização da ocorrência """
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        form = FormularioForm(request.POST, instance=ocorrencia)

        if form.is_valid():
            form.save()
            messages.success(request, "Ocorrência atualizada com sucesso!")
            return redirect('telaDetalhesChamado', id=ocorrencia.id)
        
        messages.error(request, "Erro ao atualizar a ocorrência. Verifique os campos.")
        return render(request, self.template_name, {'form': form, 'ocorrencia': ocorrencia})

class PerfilView(LoginRequiredMixin, View):
    def get(self, request, username):
        if username != request.user.nome:
            messages.error(request, "Este não é o seu perfil")
            return redirect('home')

        form = PasswordChangeForm(user=request.user)
        return render(request, 'TelaPerfil.html', {
            'user': request.user,
            'form': form
        })

    def post(self, request, username):
        if username != request.user.nome:
            messages.error(request, "Este não é o seu perfil")
            return redirect('home')

        form_type = request.POST.get("form_type")

        if form_type == "alterar_senha":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Sua senha foi alterada com sucesso!")
                return redirect('telaPerfil', username=request.user.nome)
            else:
                messages.error(request, "Erro ao alterar senha. Verifique os dados.")

        elif form_type == "excluir_perfil":
            user = request.user
            user.delete()
            messages.success(request, "Sua conta foi excluída com sucesso!")
            return redirect('home')  # Redireciona para a página inicial após exclusão

        form = PasswordChangeForm(user=request.user)  # Recarrega o formulário se der erro
        return render(request, 'TelaPerfil.html', {'user': request.user, 'form': form})

class FormularioView(View):

    def get(self, request):
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'Nome_Autor': request.user.nome,
                'Celular_Autor': request.user.telefone,  # Supondo que o celular esteja no perfil
                'Telefone_Autor': request.user.telefone_fixo,  # Supondo que o telefone esteja no perfil
                'Relacao_Autor': request.user.relacao_ufrpe,  # Supondo que você tenha este campo
            }
        form = FormularioForm(initial=initial_data)
        formset = ImagemFormSet()
        return render(request, 'Form.html', {'form': form, 'formset': formset})


    def post(self, request):
        form = FormularioForm(request.POST, request.FILES)  # Processa os dados do formulário
        formset = ImagemFormSet(request.POST, request.FILES)  # Inclui arquivos enviados

        # Verifica se é uma requisição AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid() and formset.is_valid():
                
                ocorrencia = form.save(commit=False)
                if request.user.is_authenticated:
                    ocorrencia.Autor = request.user
                else:
                    ocorrencia.Autor = get_or_create_anonymous_user()
                ocorrencia.save()

                imagens = formset.save(commit=False)
                for imagem in imagens:
                    imagem.IdOcorrencia = ocorrencia
                    imagem.save()

            # Redireciona ou limpa o formulário após salvar com sucesso
            form = FormularioForm()  # Reseta o formulário
            formset = ImagemFormSet()  # Reseta o formset

            return JsonResponse({'success': True, 'message': 'Formulário enviado com sucesso!', 'redirect_url': reverse('home')})

        else:

            # Caso os formulários sejam inválidos, processa os erros
            error_messages = []

            # Erros do formulário principal
            if not form.is_valid():
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"Erro no campo '{field}': {error}")

            # Erros do formset
            if not formset.is_valid():
                for i, form_errors in enumerate(formset.errors):
                    for field, errors in form_errors.items():
                        for error in errors:
                            error_messages.append(f"Erro no formulário de imagem {i + 1} - campo '{field}': {error}")

            # Erros gerais do formset
            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    error_messages.append(f"Erro geral no formset de imagens: {error}")
                    
            # Retorna os erros no contexto
            return JsonResponse({'success': False, 'errors': error_messages})
        

def logout_view(request):
    logout(request)
    return redirect('home')

class CadastroView(View):

    def get(self, request):
        form = CadastroForm()  # Exibe o formulário vazio
        return render(request, 'Cadastro.html', {'form': form})

    def post(self, request):
        form = CadastroForm(request.POST, request.FILES)  # Processa os dados do formulário
        if form.is_valid():
            form.save()  # Salva os dados no banco de dados
            # Adicione uma mensagem de sucesso e redirecione para a página inicial
            return render(request, 'Cadastro.html', {'form': CadastroForm(), 'success': True, 'redirect_url': 'home'})
        return render(request, 'Cadastro.html', {'form': form, 'error': True})

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})
    
    def post(self, request):
        email = request.POST['emailLogin']
        password = request.POST['passwordLogin']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'home.html', {})
        else:
            print("Email ou senha errados")
            print(user)
            return render(request, 'home.html', {'error': 'E-mail ou senha inválidos.'})

class InformativosView(View):
    def get(self, request):
        # Busca todos os informativos ordenados pela data de criação (mais recentes primeiro)
        informativos = Informativo.objects.order_by('-data_criacao')
        
        # Passa os informativos para o contexto do template
        contexto = {
            'informativos': informativos,
        }

        # Renderiza o template com o contexto
        return render(request, 'TelaInformativos.html', contexto)

class CriarInformativoView(View):
    def get(self, request, id=None):
        if id is None:
            form = InformativoForm(user=request.user)
            contexto = {'form': form, 'informativo': None}
        else:
            informativo = Informativo.objects.get(id=id)
            form = InformativoForm(instance=informativo, user=request.user)  # Passa o usuário e o informativo
            contexto = {'form': form, 'informativo': informativo}

        return render(request, 'criarInformativos.html', contexto)

    def post(self, request, id=None):
        if id is None:
            form = InformativoForm(request.POST, request.FILES, user=request.user)
        else:
            informativo = Informativo.objects.get(id=id)
            form = InformativoForm(request.POST, request.FILES, instance=informativo, user=request.user)

        if form.is_valid():
            informativo = form.save()  # Salva o informativo
            # imagens = request.FILES.getlist('imagens')
            return redirect('gerenciarInformativos')
        else:
            return render(request, 'criarInformativos.html', {'form': form})

    
class GerenciarInformativosView(View):
    def get(self, request):
        # Busca todos os informativos ordenados pela data de criação (mais recentes primeiro)
        informativos = Informativo.objects.order_by('-data_criacao').filter(id_Autor=request.user)
        # Passa os informativos para o contexto do template
        contexto = {
            'informativos': informativos
        }

        # Renderiza o template com o contexto
        return render(request, 'gerenciarInformativos.html', contexto)
    
    def post(self, request):
        id = request.POST['id']
        informativo = Informativo.objects.get(id=id)
        informativo.excluir_informativo()
        return redirect('gerenciarInformativos')

def staff(user):
    return user.is_staff
# View que notifica um staff oua acima de um novo chamado
@login_required # precisa esta logado
@user_passes_test(staff) # precisa ser staff
def notificacoes_view(request): # envia um JSON para página para criacao do popup de notificao
    notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False)
    dados = [{
        'id': notificacao.id,
        'mensagem': notificacao.mensagem,
        'lida': notificacao.lida
    } for notificacao in notificacoes]
    return JsonResponse({'notificacoes': dados})

# View que atualiaza uma notificacao para lida
@login_required
@require_POST
def notificacao_lida(request):
    notification_id = request.POST.get("notification_id")
    if not notification_id: # Verifica o ID da notificao
        return JsonResponse({"success": False, "error": "ID não fornecido."}, status=400)
    
    try:
        notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False).update(lida=True) # marca todas as notificacoes do usuario como lidas
        Notification.objects.filter(usuario=request.user, lida=True).delete() # apaga do banco todas as mensagens lidas
        return JsonResponse({"success": True, "notificacoes_lidas": notificacoes}) # envia resposta JSON a pagina
    except Notificacao.DoesNotExist:
        return JsonResponse({"success": False, "error": "Notificação não encontrada."}, status=404)
