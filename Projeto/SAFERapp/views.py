from django.views.generic import View
from django.shortcuts import render, redirect
from SAFERapp.beans.Forms import FormularioForm

# Create your views here.

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

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})