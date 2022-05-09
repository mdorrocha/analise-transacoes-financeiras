from django.urls import path
from importacoes import views

urlpatterns = [
    path('', views.importar_arquivo, name='importar-arquivo'),
    path('<int:id>', views.detalhar_importacao, name='detalhar-importacao'),
    path('analisar-transacao', views.analisar_transacao, name='analisar-transacao'),
]
