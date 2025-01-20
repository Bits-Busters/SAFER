from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from SAFERapp.beans.Forms import FormularioForm, FilterForm, ImagemFormSet
from SAFERapp.beans.Forms import CadastroForm
from SAFERapp.beans.Ocorrencia import Ocorrencia
from .models import CustomUser


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
    return render(request, 'TelaDetalhesChamado.html', {"ocorrencia": ocorrencia})

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

        if form.is_valid() and formset.is_valid():
            ocorrencia = form.save(commit=False)  # Cria a instância sem salvar ainda

            # Associa o autor à ocorrência
            if request.user.is_authenticated:
                ocorrencia.Autor = request.user
            else:
                try:
                    ocorrencia.Autor = CustomUser.objects.get(nome='Anônimo Usuário')
                except CustomUser.DoesNotExist:
                    autor_anônimo = CustomUser.objects.create(
                        email='anonimo@example.com',  # Email genérico
                        nome="Anônimo Usuário",
                        telefone="000000000",
                        telefone_fixo="000000000",
                        relacao_ufrpe="VISITANTE",  # Valor padrão
                        tipo_usuario="COMUM",
                        is_active=True
                    )
                    ocorrencia.Autor = autor_anônimo

            # Salva a ocorrência
            ocorrencia.save()

            # Associa as imagens à ocorrência e salva
            imagens = formset.save(commit=False)
            for imagem in imagens:
                imagem.IdOcorrencia = ocorrencia  # Relaciona cada imagem à ocorrência
                imagem.save()

            # Redireciona ou limpa o formulário após salvar com sucesso
            form = FormularioForm()  # Reseta o formulário
            formset = ImagemFormSet()  # Reseta o formset
            return render(request, 'Form.html',
                          {'form': form, 'formset': formset, 'success': True, 'redirect_url': 'home'})
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

            print(error_messages)

            # Retorna os erros no contexto
            return render(request, 'Form.html', {
                'form': form,
                'formset': formset,
                'error': True,
                'error_messages': error_messages,
            })


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
            return redirect('telaUsuario', username=user.nome)
        else:
            print("Email ou senha errados")
            print(user)
            return render(request, 'home.html', {'error': 'E-mail ou senha inválidos.'})