from django.contrib import admin
from importacoes.models import Transacao, Importacao

# Register your models here.

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    pass

@admin.register(Importacao)
class ImportacaoAdmin(admin.ModelAdmin):
    pass

