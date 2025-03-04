from django.forms import inlineformset_factory

from SAFERapp.beans.Observacoes import Observacoes
from SAFERapp.beans.Enums import Registro, Local, StatusChamado
from SAFERapp.beans.Imagens import Imagens 
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.beans.Informativos import Informativo
from SAFERapp.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms.models import inlineformset_factory

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['relacao_ufrpe', 'tipo_usuario']  # Apenas os campos editáveis


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
    Data = forms.DateField(
        required=False,
        label="Data",
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
    extra=5,  # Quantidade de campos extras para imagens
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