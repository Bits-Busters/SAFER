from django.conf import settings
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count


from SAFERapp.beans.Enums import StatusChamado
from SAFERapp.beans.Forms import CustomPasswordChangeForm, FormularioForm, FilterForm, ImagemFormSet, CustomUserForm, UserFilterFormRelatorio, OcorrenciaFilterFormRelatorio
from SAFERapp.beans.Forms import CadastroForm, InformativoForm, ObservacaoForm
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.beans.Informativos import Informativo
from SAFERapp.beans.Observacoes import Observacoes
from SAFERapp.models import Notificacao
from .models import CustomUser, get_or_create_anonymous_user

from SAFERapp.beans.Imagens import Imagens


# Create your views here.
@login_required
def relatorio_view(request):
    # Inicializar os formulários com os dados GET
    user_form = UserFilterFormRelatorio(request.GET or None)
    ocorrencia_form = OcorrenciaFilterFormRelatorio(request.GET or None)

    # Obter todos os usuários e ocorrências
    ocorrencias = Ocorrencia.objects.all()
    usuarios = CustomUser.objects.all()

    # Contar o número total de usuários e ocorrências
    quantidadeUsuarios = usuarios.count()
    quantidadeOcorrencias = ocorrencias.count()

    # Filtragem de Ocorrências
    if ocorrencia_form.is_valid():
        # Filtrar por Data Inicial
        data_inicial = ocorrencia_form.cleaned_data.get('DataInicial')
        if data_inicial:
            ocorrencias = ocorrencias.filter(DataHora__gte=data_inicial)

        # Filtrar por Data Final
        data_final = ocorrencia_form.cleaned_data.get('DataFinal')
        if data_final:
            ocorrencias = ocorrencias.filter(DataHora__lte=data_final)

        # Filtrar por Tipo de Caso
        tipo_caso = ocorrencia_form.cleaned_data.get('TipoCaso')
        if tipo_caso:
            ocorrencias = ocorrencias.filter(Tipo_Caso=tipo_caso)

    # Filtragem de Usuários
    if user_form.is_valid():
        # Filtrar por Relação com a UFRPE
        relacao_ufrpe = user_form.cleaned_data.get('relacao_ufrpe')
        if relacao_ufrpe:
            usuarios = usuarios.filter(relacao_ufrpe=relacao_ufrpe)

        # Filtrar por Tipo de Usuário
        tipo_usuario = user_form.cleaned_data.get('tipo_usuario')
        if tipo_usuario:
            usuarios = usuarios.filter(tipo_usuario=tipo_usuario)

    quantidadeUsuariosFiltrados = usuarios.count()
    quantidadeOcorrenciasFiltrados = ocorrencias.count()

    # Gerando os dados para gráficos (exemplo)
    tipo_ocorrencia_count = ocorrencias.values('Tipo_Caso').annotate(total=Count('Tipo_Caso'))
    status_ocorrencia_count = ocorrencias.values('Status').annotate(total=Count('Status'))

    # Preparando os dados para o gráfico (ocorrências por tipo de caso)
    tipos = [item['Tipo_Caso'] for item in tipo_ocorrencia_count]
    tipo_counts = [item['total'] for item in tipo_ocorrencia_count]

    # Preparando os dados para o gráfico (ocorrências por status)
    status = [item['Status'] for item in status_ocorrencia_count]
    status_counts = [item['total'] for item in status_ocorrencia_count]

    print(tipos)
    print("\n")
    print(tipo_counts)
    print("\n")
    print(status)
    print("\n")
    print(status_counts)

    # Retornar os resultados para o template
    return render(request, 'TelaRelatorio.html', {
        'user_form': user_form,
        'ocorrencia_form': ocorrencia_form,
        'ocorrencias': ocorrencias,
        'usuarios': usuarios,
        'quantidadeUsuarios': quantidadeUsuarios,
        'quantidadeOcorrencias': quantidadeOcorrencias,
        'quantidadeUsuariosFiltrados' : quantidadeUsuariosFiltrados,
        'quantidadeOcorrenciasFiltrados' : quantidadeOcorrenciasFiltrados,
        'tipos': tipos,
        'status_chamado': status,
        'tipo_counts': tipo_counts,
        'status_counts': status_counts,
    })


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
            ocorrencia = ocorrencia.filter(Tipo_Caso=tipoCaso)

        dataIncial = form.cleaned_data.get('DataInicial')  # Aqui você acessa a data corretamente
        if dataIncial:
            ocorrencia = ocorrencia.filter(DataHora__gte=dataIncial)  # Filtra apenas pela data, não pelo horário

        dataFinal = form.cleaned_data.get('DataFinal')  # Aqui você acessa a data corretamente
        if dataFinal:
            ocorrencia = ocorrencia.filter(DataHora__lte=dataFinal)  # Filtra apenas pela data, não pelo horário

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

@login_required
def editar_usuario(request, usuario_email):
    usuario = get_object_or_404(CustomUser, email=usuario_email)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gerenciarUsuarios')  # Redireciona de volta para a lista de usuários
    else:
        form = CustomUserForm(instance=usuario)

    return render(request, 'DetalhesUsuario.html', {'form': form, 'usuario': usuario})

@login_required
def deletar_usuario(request, usuario_email):
    usuario = get_object_or_404(CustomUser, email=usuario_email)
    
    # Verifica se o usuário que está tentando excluir não é ele mesmo
    if usuario == request.user:
        return redirect('gerenciarUsuarios')

    usuario.delete()
    return redirect('gerenciarUsuarios')

@login_required
def telaGerenciarUsuarios(request):
    usuarios = CustomUser.objects.all().order_by('nome')
    # Cria um objeto Paginator para dividir as ocorrências em páginas com 5 itens cada
    paginator = Paginator(usuarios, 5)  # 5 ocorrências por página

    # Obtém o número da página atual
    page_number = request.GET.get('page')  # Pode vir da URL (por exemplo: ?page=2)
    page_obj = paginator.get_page(page_number)

    # Renderiza a página com as ocorrências paginadas
    return render(request, 'TelaGerenciarUsuarios.html', {'page_obj': page_obj})

def telaUsuario(request, username):
    if username != request.user.nome:
        messages.error(request, "Este não era o seu perfil")
        return render(request, 'home.html')
    return render(request, 'TelaUsuario.html')

class TelaDetalhesChamadoView(View):
    resgatistas = ['admin', 'gestor', 'analista']

    def get(self, request, id):
        ocorrencia = get_object_or_404(Ocorrencia, id=id)
        ocorrenciaImagem = Imagens.objects.filter(IdOcorrencia=ocorrencia)
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
            messages.success(request, "Chamado aceito com sucesso!")
            return redirect('telaDetalhesChamado', ocorrencia.id)

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

        elif form_type == "deletar_ocorrencia":
            print(f"Usuário: {request.user}, Autor da Ocorrência: {ocorrencia.Autor}")
            if request.user == ocorrencia.Autor or request.user.tipo_usuario == 'admin':
                ocorrencia.delete()
                messages.success(request, "Ocorrência excluída com sucesso!")
                return redirect('home')
            else:
                messages.error(request, "Você não tem permissão para excluir esta ocorrência.")

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
        # Recupera a ocorrência existente
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        
        # Preenche o formulário com os dados da ocorrência
        form = FormularioForm(instance=ocorrencia)
        
        # Obtém as imagens associadas à ocorrência
        imagens = Imagens.objects.filter(IdOcorrencia=ocorrencia)
        
        # Adiciona um print para depuração - ver quantas imagens e seus nomes
        print(f'Número de imagens associadas à ocorrência {ocorrencia_id}: {len(imagens)}')
        for imagem in imagens:
            print(f'Imagem: {imagem.Image.name}')  # Mostra o nome do arquivo de imagem
        
        # Cria o formset para as imagens, passando as imagens já associadas
        formset = ImagemFormSet(queryset=imagens, instance=ocorrencia)  # Passa o queryset das imagens para o formset

        # Adiciona um print para depuração - ver o conteúdo do formset
        print("Conteúdo do formset:")
        for idx, imagem_form in enumerate(formset):
            print(f"Formulário {idx+1} no formset:")
            for field in imagem_form:
                print(f"  Campo: {field.name} | Valor: {field.value()}")
        
        return render(request, 'TelaAtualizarDetalhesChamado.html', {
            'form': form,
            'formset': formset,  # Passa o formset para o template
            'ocorrencia': ocorrencia,
            'resgatistas': self.resgatistas
        })

    
    def post(self, request, ocorrencia_id):
        """ Processa os dados do formulário """
        # Recupera a ocorrência existente
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        
        # Cria ou atualiza os formulários com os dados POST
        form = FormularioForm(request.POST, request.FILES, instance=ocorrencia)  # Associando a ocorrência para atualização
        formset = ImagemFormSet(request.POST, request.FILES, instance=ocorrencia)  # Passa o queryset das imagens já existentes
        
        print("Conteúdo do formset:")
        for idx, imagem_form in enumerate(formset):
            print(f"Formulário {idx+1} no formset:")
            for field in imagem_form:
                print(f"  Campo: {field.name} | Valor: {field.value()}")
        
        print("Ajax")
        # Verifica se é uma requisição AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid() and formset.is_valid():
                # Salva ou atualiza a ocorrência
                ocorrencia = form.save(commit=False)
                if request.user.is_authenticated:
                    ocorrencia.Autor = request.user
                else:
                    ocorrencia.Autor = get_or_create_anonymous_user()
                ocorrencia.save()  # Salva a ocorrência (atualização)

                # Atualiza as imagens
                imagens = formset.save(commit=False)
                for imagem in imagens:
                    imagem.IdOcorrencia = ocorrencia  # Atribui a imagem à ocorrência correta
                    imagem.save()  # Salva ou atualiza as imagens

                # 🔥 ESSA PARTE AQUI FAZ A REMOÇÃO FUNCIONAR
                for obj in formset.deleted_objects:
                    obj.delete()

                print("Sucesso")
                # Retorna uma resposta de sucesso
                return JsonResponse({
                    'success': True, 
                    'message': 'Formulário enviado com sucesso!', 
                    'redirect_url': reverse('home')
                })
            else:
                # Se o formulário ou o formset estiverem inválidos, coleta os erros
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
        return JsonResponse({'success': False, 'message': 'Erro desconhecido'})


class PerfilView(LoginRequiredMixin, View):
    def get(self, request, username):
        if username != request.user.nome:
            messages.error(request, "Este não é o seu perfil")
            return redirect('home')

        form = CustomPasswordChangeForm(user=request.user)
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
            form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save(request.user)  # Salva a nova senha no usuário
                messages.success(request, "Sua senha foi alterada com sucesso!")
                return redirect('telaPerfil', username=request.user.nome)  # Aqui você pode redirecionar após o sucesso
            else:
                messages.error(request, "Erro ao alterar senha. Verifique os dados.")
                # Renderize novamente a página com o formulário contendo os erros
                return render(request, 'TelaPerfil.html', {
                    'user': request.user,
                    'form': form
                })

        elif form_type == "excluir_perfil":
            user = request.user
            user.delete()
            messages.success(request, "Sua conta foi excluída com sucesso!")
            return redirect('home')  # Redireciona para a página inicial após exclusão

def deletar_ocorrencia(request, id):
    if request.method == 'POST':
        ocorrencia = get_object_or_404(Ocorrencia, id=id)
        
        # Verifique se o usuário tem permissão para deletar
        if request.user.tipo_usuario == 'admin' or ocorrencia.Resgatista == request.user or ocorrencia.Autor == request.user:
            ocorrencia.delete()
            # Redirecione para uma página de sucesso ou listagem de ocorrências
            return redirect('home')  # Altere para a URL desejada
    
    return redirect('home')  # Redirecione se não for uma requisição POST ou se o usuário não tiver permissão

class FormularioView(View):

    def get(self, request):
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'Nome_Autor': request.user.nome,
                'Celular_Autor': request.user.telefone,
                'Telefone_Autor': request.user.telefone_fixo,
                'Relacao_Autor': request.user.relacao_ufrpe,
            }
        form = FormularioForm(initial=initial_data)
        formset = ImagemFormSet()
        return render(request, 'Form.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = FormularioForm(request.POST, request.FILES)
        formset = ImagemFormSet(request.POST, request.FILES)

        # Verifica se é uma requisição AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid() and formset.is_valid():
                # Acesse form.cleaned_data somente após a validação
                print("Dados do form:", form.cleaned_data)
                form.instance.Localizacao_x = request.POST.get('Localizacao_x')
                form.instance.Localizacao_y = request.POST.get('Localizacao_y')
                ocorrencia = form.save(commit=False)
                if request.user.is_authenticated:
                    ocorrencia.Autor = request.user
                else:
                    ocorrencia.Autor = get_or_create_anonymous_user()
                ocorrencia.save()

                imagens = formset.save(commit=False)

                # Verificar e exibir a quantidade de imagens e os nomes
                imagens_salvas = []
                for imagem in imagens:
                    imagem.IdOcorrencia = ocorrencia
                    imagem.save()
                
                    # Adicionar o nome da imagem à lista
                    imagens_salvas.append(imagem.Image.name)
            
                # Exibir a quantidade de imagens e seus nomes
                print(f"Quantidade de imagens recebidas: {len(imagens_salvas)}")
                print("Nomes das imagens recebidas:", imagens_salvas)

                for imagem in imagens:
                    imagem.IdOcorrencia = ocorrencia
                    imagem.save()

                # Verificar se o request.FILES contém todas as imagens
                print("Arquivos recebidos em request.FILES:")
                for key, value in request.FILES.items():
                    print(f"{key}: {value.name}")  # Exibe o nome de cada arquivo enviado

                # Reseta o formulário após salvar
                form = FormularioForm()
                formset = ImagemFormSet()

                return JsonResponse({
                    'success': True, 
                    'message': 'Formulário enviado com sucesso!', 
                    'redirect_url': reverse('home')
                })
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

                return JsonResponse({'success': False, 'errors': error_messages})

        else:
            return JsonResponse({'success': False, 'message': 'Requisição inválida'})
        

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
            messages.success(request, "Login efetuado com sucesso!")
            return render(request, 'home.html')
        else:
            print("Email ou senha errados")
            print(user)
            messages.error(request, "E-mail ou senha inválidos.")
            return render(request, 'home.html')

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
            # Mensagem de sucesso: criação ou atualização
            if id is None:
                messages.success(request, "Informativo criado com sucesso!")
            else:
                messages.success(request, "Informativo atualizado com sucesso!")

            return redirect('gerenciarInformativos')  # Redireciona para a lista de informativos
        else:
            # Mensagem de erro: formulário inválido
            messages.error(request, "Erro ao criar o informativo. Verifique os dados.")
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
        # Verifica se o usuário tem permissão para excluir
        informativo_id = request.POST['id']
        informativo = Informativo.objects.get(id=informativo_id)
        
        # Permissões: Só pode excluir se for o autor ou um administrador
        if request.user == informativo.id_Autor or request.user.tipo_usuario == 'admin':
            informativo.delete()
            messages.success(request, "Informativo excluído com sucesso!")
        else:
            messages.error(request, "Você não tem permissão para excluir este informativo.")

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
        Notificacao.objects.filter(usuario=request.user, lida=True).delete() # apaga do banco todas as mensagens lidas
        return JsonResponse({"success": True, "notificacoes_lidas": notificacoes}) # envia resposta JSON a pagina
    except Notificacao.DoesNotExist:
        return JsonResponse({"success": False, "error": "Notificação não encontrada."}, status=404)





def render_mapa_calor(request):
        import folium
        import numpy as np
        from folium.plugins import HeatMap
        from django.http import HttpResponse


        pontos = list(Ocorrencia.objects.values_list('Localizacao_x', "Localizacao_y"))
        coordenadas = np.array(pontos)

        # Centro do mapa
        latitude = np.mean(coordenadas[:, 0])
        logintude = np.mean(coordenadas[:, 1])

        mapa = folium.Map(location=[-8.017598865420956, -34.94933404268544], zoom_start=14.11)


        # Adição do mapa de calor
        HeatMap(coordenadas, radius=20, blur=10).add_to(mapa)

        # Retorno do mapa como HTML
        mapa_html = mapa._repr_html_()
        return HttpResponse(mapa_html)
