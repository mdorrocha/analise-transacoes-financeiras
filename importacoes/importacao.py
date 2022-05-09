from abc import ABC, abstractmethod
from datetime import datetime
from django.forms import ValidationError
from importacoes.models import Importacao
from bs4 import BeautifulSoup
from collections import OrderedDict

# colunas do arquivo csv    
columns_order = (
    'banco_origem',
    'agencia_origem',
    'conta_origem',
    'banco_destino',
    'agencia_destino',
    'conta_destino',
    'valor_transacao',
    'data_hora_transação'
    )        

class Validation(ABC):
    def __init__(self, file):
        self.file = file
        self._data_transacao = None
        self._linhas_validas = []          
    
    def _validate_row(self, columns):
        # a data da transação é lida da primeira linha do arquivo
        # se a data nas linhas seguintes forem diferentes as mesmas devem ser descartadas
        if len(columns) == len(columns_order) and all(columns):
            # converte string para um objeto date
            parsed_date = datetime.fromisoformat(columns[7]).date()
            if not self._data_transacao:
                self._data_transacao = parsed_date
                # testa se a data da transação já foi importada
                if Importacao.objects.filter(data_transacao=self._data_transacao):
                    data_formatada = self._data_transacao.strftime('%d/%m/%Y')
                    raise ValidationError(f'As transações em {data_formatada} já foram importadas')
            if self._data_transacao == parsed_date:
                linha_valida = dict()
                for key, value in enumerate(columns_order):
                    linha_valida[value] = columns[key]
                self._linhas_validas.append(linha_valida)        

    @abstractmethod
    def extract_valid_rows():
        pass

class ValidationCSV(Validation):

    def __init__(self, file):
        super().__init__(file)

    def extract_valid_rows(self):      
        for row in self.file:
            columns = row.decode('utf-8').rstrip('\n').split(',')
            super()._validate_row(columns)
        return self._linhas_validas     
    

class ValidationXML(Validation):

    def __init__(self, file):
        super().__init__(file)

    def extract_valid_rows(self):
        soup = BeautifulSoup(self.file, 'xml')
        for row_xml in soup.find_all('transacao'):
            row = []
            row.append(row_xml.origem.banco.get_text())
            row.append(row_xml.origem.agencia.get_text())
            row.append(row_xml.origem.conta.get_text())
            row.append(row_xml.destino.banco.get_text())
            row.append(row_xml.destino.agencia.get_text())
            row.append(row_xml.destino.conta.get_text())
            row.append(row_xml.valor.get_text())
            row.append(row_xml.data.get_text())
            super()._validate_row(row)
        return self._linhas_validas

FORMATOS_SUPORTADOS = OrderedDict(
    [
        ('csv', ValidationCSV),
        ('xml', ValidationXML)
    ]
)
    