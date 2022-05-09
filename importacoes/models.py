from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

class Importacao(models.Model):
    class Meta:
        verbose_name = 'Importação'
        verbose_name_plural = 'Importações'
    
    data_hora_importacao = models.DateTimeField(verbose_name='Data e hora da importação', auto_now_add=True)
    data_transacao = models.DateField(verbose_name='Data da transação')
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)


class Transacao(models.Model):
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    banco_origem = models.CharField(verbose_name='Banco de origem', max_length=100)
    agencia_origem = models.CharField(verbose_name='Agência de origem', max_length=6)
    conta_origem = models.CharField(verbose_name='Conta de origem', max_length=10)
    banco_destino = models.CharField(verbose_name='Banco de destino', max_length=100)
    agencia_destino = models.CharField(verbose_name='Agência de destino', max_length=6)
    conta_destino = models.CharField(verbose_name='Conta de destino', max_length=10)
    valor_transacao = models.DecimalField(verbose_name='Valor da transação', max_digits=10, decimal_places=2)
    data_hora_transação = models.DateTimeField(verbose_name='Data e hora da transação')
    importacao = models.ForeignKey(Importacao, verbose_name='Importação', on_delete=models.CASCADE)

    def eh_transacao_suspeita(self, limite=100000.00):
        """
        Uma transação deve ser considerada suspeita se o seu valor 
        for igual ou superior a R$100.000,00.
        """
        return self.valor_transacao >= limite
    
    @staticmethod
    def listar_transacoes_por_mes_ano(periodo):
        # periodo para análise no formato mm/yy
        periodo = periodo.split('/')
        # obtem todas as importações do período analisado
        importacoes = Importacao.objects.filter(data_transacao__month=periodo[0], data_transacao__year=periodo[1])
        # obtem todas as transações do período analisado
        transacoes = Transacao.objects.filter(importacao__in=importacoes)
        return transacoes

    @staticmethod
    def listar_atividades_suspeitas(periodo, limite=100000.00):
        TIPO_ANALISE_CONTA = 'conta'
        TIPO_ANALISE_AGENCIA = 'agencia'
        agrupar_por = {
            TIPO_ANALISE_CONTA: ('banco', 'agencia', 'conta'),
            TIPO_ANALISE_AGENCIA: ('banco', 'agencia')
        }
        analises = {
                TIPO_ANALISE_CONTA: {
                    'entrada': ('banco_origem', 'agencia_origem', 'conta_origem'),
                    'saida': ('banco_destino', 'agencia_destino', 'conta_destino'),
                },
                TIPO_ANALISE_AGENCIA: {
                    'entrada': ('banco_origem', 'agencia_origem'),
                    'saida': ('banco_destino', 'agencia_destino'),
                }        
        }
        contas_supeitas = []
        agencias_suspeitas = []
        atividades_suspeitas = {
            'contas_suspeitas': contas_supeitas,
            'agencias_suspeitas': agencias_suspeitas
        }
        transacoes = Transacao.listar_transacoes_por_mes_ano(periodo)
        # itera pelo tipo de análise (conta ou agência)
        for tipo, tipo_mov in analises.items(): 
            # itera por tipo movimentação (entrada ou saída)
            for tipo_mov, value in tipo_mov.items(): 
                movimentacoes = transacoes.values(*value).annotate(Sum('valor_transacao'))
                # pesquisa por atividades suspeitas
                for movimentacao in movimentacoes:
                    if movimentacao['valor_transacao__sum'] >= limite:
                        analise = {
                            'valor_transacao__sum': movimentacao['valor_transacao__sum'],
                            'tipo_movimentacao': tipo_mov.capitalize(),
                        }  
                        for i, v in enumerate(agrupar_por.get(tipo)):
                            analise[v] = movimentacao[value[i]]
                        if tipo == TIPO_ANALISE_CONTA:
                            contas_supeitas.append(analise)
                        else:
                            agencias_suspeitas.append(analise)
        return atividades_suspeitas