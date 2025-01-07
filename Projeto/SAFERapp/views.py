from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from SAFERapp.beans.Forms import FormularioForm
from SAFERapp.beans.Forms import CadastroForm
from SAFERapp.beans.Ocorrencia import Ocorrencia


# Create your views here.

@login_required
def telaOcorrencias(request, username):
    if username != request.user.nome:
        messages.error(request, "Este não era o seu perfil")
        return render(request, 'home.html')
    # Obtém as ocorrências do usuário logado
    ocorrencia = Ocorrencia.objects.filter(Autor=request.user).order_by('-DataHora')

    # Cria um objeto Paginator para dividir as ocorrências em páginas com 5 itens cada
    paginator = Paginator(ocorrencia, 5)  # 5 ocorrências por página

    # Obtém o número da página atual
    page_number = request.GET.get('page')  # Pode vir da URL (por exemplo: ?page=2)
    page_obj = paginator.get_page(page_number)

    # Renderiza a página com as ocorrências paginadas
    return render(request, 'TelaChamados.html', {'page_obj': page_obj})

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
        return render(request, 'Form.html', {'form': form})

    def post(self, request):
        form = FormularioForm(request.POST, request.FILES)  # Processa os dados do formulário
        if form.is_valid():
            ocorrencia = form.save(commit=False)
            if request.user is not None:
                ocorrencia.Autor = request.user
            ocorrencia.save()  # Salva os dados no banco de dados
            return redirect('home')  # Redireciona para a página de sucesso
        return render(request, 'Form.html', {'form': form})

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
            return redirect('home')  # Redireciona para a página de sucesso
        return render(request, 'Cadastro.html', {'form': form})

class HomeView(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect('telaUsuario', username=request.user.nome)
        else:
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