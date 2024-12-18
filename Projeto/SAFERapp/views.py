from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render, redirect

from SAFERapp.beans.Forms import FormularioForm
from SAFERapp.beans.Forms import CadastroForm
from SAFERapp.beans.Ocorrencia import Ocorrencia


# Create your views here.

@login_required
def TelaUsuario(request, username):
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
    return render(request, 'TelaUsuario.html', {'page_obj': page_obj})


class FormularioView(View):

    def get(self, request):
        form = FormularioForm()  # Exibe o formulário vazio
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
        if request.user is not None:
            return redirect('TelaUsuario', username=request.user.nome)
        return render(request, 'home.html', {})
    def post(self, request):
        email = request.POST['emailLogin']
        password = request.POST['passwordLogin']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('TelaUsuario', username=user.nome)
        else:
            return render(request, 'home.html', {'error': 'E-mail ou senha inválidos.'})