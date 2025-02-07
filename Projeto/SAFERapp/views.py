from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from SAFERapp.beans.Forms import FormularioForm, FilterForm, ImagemFormSet
from SAFERapp.beans.Forms import CadastroForm, InformativoForm
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.beans.Informativos import Informativo
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
        ocorrencia = Ocorrencia.objects.filter(Analista=request.user).order_by('-DataHora')
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

def telaDetalhesChamado(request, id):
    #verificar se o chamado em questão pertence ao usuario
    ocorrencia = get_object_or_404(Ocorrencia, id=id)
    ocorrenciaImagem = Imagens.objects.filter(IdOcorrencia=ocorrencia).first()
    return render(request, 'TelaDetalhesChamado.html', {"ocorrencia": ocorrencia, 'imagem': ocorrenciaImagem})

@login_required
def telaPerfil(request, username):
    if username != request.user.nome:
        messages.error(request, "Este não era o seu perfil")
        return render(request, 'home.html')
    else:
        user = request.user
        if request.method == "POST":
            form = PasswordChangeForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Sua senha foi alterada com sucesso!")
                return redirect('telaPerfil', username=request.user.nome)  # Redireciona para a página de perfil
        else:
            form = PasswordChangeForm(user=user)

        return render(request, 'TelaPerfil.html', {
            'user': user,
            'form': form
        })

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