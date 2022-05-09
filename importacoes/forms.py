from django import forms
from django.forms import ValidationError
from importacoes.importacao import FORMATOS_SUPORTADOS

class ImportacaoForm(forms.Form):
    arquivo = forms.FileField(allow_empty_file=False)

    def clean_arquivo(self): 
        arquivo = self.cleaned_data.get('arquivo')               
        file_type = arquivo.name.split('.')[1]
        if not FORMATOS_SUPORTADOS.get(file_type):
            raise ValidationError('Formato de arquivo não suportado')
        return arquivo

class AnaliseTransacaoForm(forms.Form):
    periodo = forms.CharField(
        label='Informe o mês e ano para análise', 
        max_length=30, 
        widget=forms.TextInput(
            attrs={
                "id": "datepicker",
                "autocomplete": "off"
            }
        )
    )