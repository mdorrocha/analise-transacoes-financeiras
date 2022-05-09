from django.forms import ValidationError
from importacoes.models import Importacao, Transacao
from django.core.mail import send_mail
from importacoes.importacao import FORMATOS_SUPORTADOS

def importar_arquivo(request, file):
    file_type = file.name.split('.')[1]
    Validation = FORMATOS_SUPORTADOS.get(file_type)
    obj = Validation(file)
    linhas_a_importar =  obj.extract_valid_rows()    
    # registra informações da importação e transações
    if linhas_a_importar:   
        dados_importacao = {
            'data_transacao': obj._data_transacao,
            'user': request.user
        }
        importacao = Importacao.objects.create(**dados_importacao)  
        for linha in linhas_a_importar:
            # salva as transações
            linha['importacao'] = importacao
            Transacao.objects.create(**linha)
    else:
        raise ValidationError('A importação falhou. Consulte o arquivo')

def enviar_email(user, password):
    send_mail(
        'Senha para acesso ao sistema de transações financeiras',
        'Senha para acesso ao sistema: ' + password,
        None,
        [user.email],
        fail_silently=False,
    )

def analisar_transacoes_suspeitas(periodo):  
    lista_transacoes_suspeitas = []      
    # pesquisa por transações suspeitas
    transacoes = Transacao.listar_transacoes_por_mes_ano(periodo)
    for transacao in transacoes:
        if transacao.eh_transacao_suspeita():
            lista_transacoes_suspeitas.append(transacao)
    # pesquisa por atividades suspeitas por contas e agências
    analises = Transacao.listar_atividades_suspeitas(periodo)
    analises.update({'transacoes_suspeitas': lista_transacoes_suspeitas})
    return analises