from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import render, redirect

from SAFERapp.beans.Forms import FormularioForm
from SAFERapp.beans.Forms import CadastroForm
# Create your views here.

@login_required
def TelaUsuario(request, username):
    if username != request.user.nome:
        messages.error(request, "Este não era o seu perfil")
        return render(request, 'home.html')
    return render(request, 'TelaUsuario.html')


class FormularioView(View):

    def get(self, request):
        form = FormularioForm()  # Exibe o formulário vazio
        return render(request, 'Form.html', {'form': form})

    def post(self, request):
        form = FormularioForm(request.POST, request.FILES)  # Processa os dados do formulário
        if form.is_valid():
            form.save()  # Salva os dados no banco de dados
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