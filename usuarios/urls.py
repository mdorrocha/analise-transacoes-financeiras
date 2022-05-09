from django.urls import path
from usuarios import views

urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('cadastrar', views.cadastrar_usuario, name='cadastrar-usuario'),
    path('atualizar/<int:id>', views.atualizar_usuario, name='atualizar-usuario'),
    path('remover/<int:id>', views.remover_usuario, name='remover-usuario'),
]