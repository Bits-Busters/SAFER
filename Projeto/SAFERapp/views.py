from django.views.generic import View
from django.shortcuts import render, redirect
from SAFERapp.beans.Forms import FormularioForm

# Create your views here.

class FormularioView(View):
    def get(self, request):
        if request.method == 'POST':
            form = FormularioForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')  # Página de sucesso após envio
        else:
            form = FormularioForm()

        return render(request, 'Form.html', {'form': form})

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})