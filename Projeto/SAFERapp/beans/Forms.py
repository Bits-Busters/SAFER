from django import forms
from SAFERapp.beans.Ocorrencia import Ocorrencia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FormularioForm(forms.Form):
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
        self.helper.form_tag = False  # Não renderizar a tag <form> automaticamente

        self.helper.add_input(Submit('submit', 'Enviar'))
