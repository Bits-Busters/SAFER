from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

class FormularioForm(forms.ModelForm):

    class Meta:
        model = Ocorrencia
        fields = ['Nome_Autor', 'Celular_Autor', 'Telefone_Autor', 'Relacao_Autor', 'Nome_Animal', 'Local', 'Referencia', 'Tipo_Caso', 'Descricao']
        widgets = {
            'Descricao': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }

    def __init__(self, *args, **kwargs):
        super(FormularioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True  # Não renderizar a tag <form> automaticamente

        self.helper.add_input(Submit('submit', 'Enviar'))

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

        if senha and confirmar_senha:
            if senha != confirmar_senha:
                raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        senha = self.cleaned_data['senha']
        user.set_password(senha)  # Definindo a senha criptografada

        if commit:
            user.save()
        return user