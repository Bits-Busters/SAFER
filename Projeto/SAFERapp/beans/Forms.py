from django.forms import inlineformset_factory

from SAFERapp.beans.Observacoes import Observacoes
from SAFERapp.beans.Enums import Registro, Local, StatusChamado, TipoUsuario, RelacaoUFRPE
from SAFERapp.beans.Imagens import Imagens 
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.beans.Informativos import Informativo
from SAFERapp.models import CustomUser, PasswordHistory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.hashers import make_password, check_password
from django import forms
from django.forms.models import inlineformset_factory

class CustomPasswordChangeForm(forms.Form):
    # Campos para a senha nova e confirmação
    old_password = forms.CharField(
        label=("Senha atual"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=("Digite a sua senha atual."),
    )
    new_password1 = forms.CharField(
        label=("Nova Senha"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=(
            "<br>Sua senha deve ter ao menos 8 caracteres;<br>"
            "Sua senha deve conter ao menos 1 letra maiúscula;<br>"
            "Sua senha deve conter ao menos 1 letra minúscula;<br>"
            "Sua senha deve conter ao menos 1 dígito;"
        ),
    )
    new_password2 = forms.CharField(
        label=("Confirmar Nova Senha"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=("Digite a mesma senha novamente para confirmação."),
    )

    # Adicionando o argumento 'user' no __init__
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Salva o usuário passado para uso posterior, como na validação

    # Método de validação para garantir que as senhas coincidam
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        user = self.user

        # Verifica se a senha antiga corresponde à do usuário
        if old_password:
            if not self.user.check_password(old_password):
                self.add_error("old_password", ("A senha atual está incorreta."))

        # Verifica se as senhas coincidem
        if password1 and password2:
            if password1 != password2:
                self.add_error('new_password2', ("As senhas não coincidem."))

        # Validar a nova senha usando seus próprios critérios, se necessário
        if password1:
            password_history = user.password_history.all()  # Obtém as últimas 5 senhas
            for entry in password_history:
                if check_password(password1, entry.password_hash):
                    self.add_error("new_password1", ("A nova senha não pode ser igual a nenhuma das últimas 5 senhas."))

            if self.user.check_password(password1):
                self.add_error("new_password1", ("A nova senha não pode ser igual à senha atual."))
            if len(password1) < 8:
                self.add_error('new_password1', ("A senha deve ter pelo menos 8 caracteres."))
            if not any(char.isdigit() for char in password1):
                self.add_error('new_password1', ("A senha deve conter pelo menos um número."))
            if not any(char.islower() for char in password1):
                self.add_error('new_password1', ("A senha deve conter pelo menos uma letra minúscula."))
            if not any(char.isupper() for char in password1):
                self.add_error('new_password1', ("A senha deve conter pelo menos uma letra maiúscula."))

        return cleaned_data

    # Método para salvar a nova senha
    def save(self, user, commit=True):
        user.set_password(self.cleaned_data["new_password1"])
        # Salva o hash da nova senha no histórico de senhas
        password_hash = make_password(self.cleaned_data["new_password1"])
        PasswordHistory.objects.create(user=user, password_hash=password_hash)

        # Limita o histórico de senhas para as últimas 5
        # Deleta as senhas anteriores quando o número de entradas excede 5
        password_history = user.password_history.all()
        if password_history.count() > 5:
            oldest_password = password_history.last()  # A senha mais antiga estará no final
            oldest_password.delete()  # Exclui a senha mais antiga
        if commit:
            user.save()
        return user

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nome', 'relacao_ufrpe', 'telefone', 'telefone_fixo', 'tipo_usuario']

class UserFilterFormRelatorio(forms.Form):
    relacao_ufrpe = forms.ChoiceField(
        required=False,
        label="Relação com a UFRPE",
        choices=[('', 'Todos')] + RelacaoUFRPE.choices,  # Adiciona a opção "Todos"
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_usuario = forms.ChoiceField(
        required=False,
        label="Tipo de usuário",
        choices=[('', 'Todos')] + TipoUsuario.choices,  # Adiciona a opção "Todos"
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class OcorrenciaFilterFormRelatorio(forms.Form):
    DataInicial = forms.DateField(
        required=False,
        label="Data Inicial",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    DataFinal = forms.DateField(
        required=False,
        label="Data Final",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    TipoCaso = forms.ChoiceField(
        required=False,
        label="Tipo de Caso",
        choices=[('', 'Todos')] + Registro.choices,  # Adiciona a opção "Todos"
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class InformativoForm(forms.ModelForm):
    class Meta:
        model = Informativo
        fields = ['titulo', 'corpo', 'imagens']
    
        widgets = {
            'corpo': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'imagens': forms.ClearableFileInput(attrs={'style': 'font-size: 12px; display: block; width: 100%; height: 100%; padding: .375rem .75rem; font-weight: 400; line-height: 1.5; color: #495057; background-color: #fff; background-clip: padding-box; border: 1px solid #ced4da; border-radius: .25rem; transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;','required':False}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Recebe o usuário
        super(InformativoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True

        self.helper.add_input(Submit('submit', 'Enviar'))

    def save(self, commit=True):
        informativo = super().save(commit=False)
        if self.user:  # Atribui o autor apenas se o usuário for fornecido
            informativo.id_Autor = self.user
        if commit:
            informativo.save()
        return informativo

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = [
            'Nome_Autor', 'Celular_Autor', 'Telefone_Autor', 'Relacao_Autor',
            'Nome_Animal', 'Local', 'Referencia', 'Tipo_Caso', 'Descricao', 'Status'
        ]
        widgets = {
            'Descricao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super(FormularioForm, self).__init__(*args, **kwargs)

        required_fields = [
            'Nome_Autor', 'Celular_Autor', 'Relacao_Autor', 
            'Nome_Animal', 'Local', 'Referencia', 'Tipo_Caso', 
            'Descricao'
        ]
        
        for field in required_fields:
            self.fields[field].required = True

        non_required_fields = ['Telefone_Autor', 'Status']
        for field in non_required_fields:
            self.fields[field].required = False
        
        # Se for uma nova ocorrência, defina o status automaticamente como "aberto"
        if not self.instance.pk:  # Verifica se é uma nova ocorrência (sem PK)
            self.fields['Status'].initial = StatusChamado.ABERTO
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Enviar'))

    def save(self, commit=True):
        instancia = super().save(commit=False)
        
        # Se a ocorrência for nova, defina o status como "aberto"
        if not self.instance.pk:
            instancia.Status = StatusChamado.ABERTO
        
        if commit:
            instancia.save()
        
        return instancia

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label='Senha', min_length=8)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha', min_length=8)

    class Meta:
        model = CustomUser
        fields = ['nome', 'email', 'telefone', 'telefone_fixo', 'relacao_ufrpe']

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True  # Não renderizar a tag <form> automaticamente

        self.helper.add_input(Submit('submit', 'Enviar'))

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        senha = self.cleaned_data['senha']
        user.set_password(senha)  # Definindo a senha criptografada

        if commit:
            user.save()
        return user

class FilterForm(forms.Form):
    Animal = forms.CharField(
        required=False,
        label="Animal",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do animal'})
    )
    DataInicial = forms.DateField(
        required=False,
        label="Data Inicial",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    DataFinal = forms.DateField(
        required=False,
        label="Data Final",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    TipoCaso = forms.ChoiceField(
        required=False,
        label="Tipo de Caso",
        choices=[('', 'Todos')] + Registro.choices,  # Adiciona a opção "Todos"
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Local = forms.ChoiceField(
        required=False,
        label="Local",
        choices=[('', 'Todos')] + Local.choices,  # Adiciona a opção "Todos"
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagens
        fields = ['Image']
        widgets = {
            'Image': forms.ClearableFileInput(attrs={
            'style': '''
                font-size: 12px;
                display: block;
                width: 100%;
                height: 100%;
                padding: .375rem .75rem;
                font-weight: 400;
                line-height: 1.5;
                color: #495057;
                background-color: #fff;
                background-clip: padding-box;
                border: 1px solid #ced4da;
                border-radius: .25rem;
                transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
            ''',
            }),
        }

ImagemFormSet = inlineformset_factory(
    Ocorrencia,  # Modelo pai
    Imagens,      # Modelo filho
    form=ImagemForm,  # Campos do modelo Imagem
    extra=3,  # Quantidade de campos extras para imagens
    can_delete=True  # Permite deletar imagens existentes
)

class ObservacaoForm(forms.ModelForm):
    class Meta:
        model = Observacoes
        fields = ['corpo']  # Campos do formulário

        widgets = {
            'corpo': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control', 'placeholder': 'Adicione uma observação...'})
        }

    def __init__(self, *args, **kwargs):
        super(ObservacaoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Enviar'))