from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from importacoes.forms import ImportacaoForm, AnaliseTransacaoForm
from importacoes.models import Importacao, Transacao
from importacoes import utils
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def index(request):
    return redirect('importar-arquivo')

@login_required(login_url='login')
def importar_arquivo(request):
    importacoes = Importacao.objects.all().order_by('-data_transacao')
    form = ImportacaoForm()
    if request.method == 'POST':
        form = ImportacaoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['arquivo']
            try:
                utils.importar_arquivo(request, file)
                messages.add_message(request, messages.SUCCESS, 'A importação do arquivo foi realizada com sucesso')
            except ValidationError as ex:
                messages.add_message(request, messages.ERROR, ex.message)
    context = {'form': form, 'importacoes': importacoes}
    return render(request, 'importacao.html', context)  

@login_required(login_url='login')
def detalhar_importacao(request, id):
    importacao = Importacao.objects.get(pk=id)
    transacoes = Transacao.objects.filter(importacao=importacao)
    context = {'importacao': importacao, 'transacoes': transacoes}
    return render(request, 'detalhar-importacao.html', context)
    
@login_required(login_url='login')
def analisar_transacao(request):
    form = AnaliseTransacaoForm()
    context = {'form': form}
    if request.method == 'POST':
        form = AnaliseTransacaoForm(request.POST)
        if form.is_valid():
            periodo = request.POST.get('periodo')
            context.update(utils.analisar_transacoes_suspeitas(periodo))
        else:
            context = {'form': form}
    return render(request, 'analisar-transacao.html', context)