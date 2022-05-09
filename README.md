# Sistema de controle de transações financeiras

## Tópicos

:small_blue_diamond: [Descrição do Projeto](#Descrição-do-Projeto)

:small_blue_diamond: [Funcionalidades](#Funcionalidades)

:small_blue_diamond: [Tecnologias utilizadas](#Tecnologias-utilizadas)

:small_blue_diamond: [Acesso ao Projeto](#Acesso-ao-Projeto)


# Descrição do Projeto

Este projeto foi proposto no Challenges Alura Backend 3 e o objetivo é desenvolver uma aplicação Web tradicional(server-side) para realizar análise de transações financeiras e identificar possíveis transações suspeitas. 

# Funcionalidades

:heavy_check_mark: Importação de arquivos

A primeira funcionalidade é uma tela para importação de arquivos CSV ou XML contendo transações financeiras. Após a leitura do arquivo, as informações de cada transação são armazenadas no banco de dados e também é mantido o histórico das importações. As seguintes regras devem ser atendidas:

* Se o arquivo que foi feito upload estiver vazio, uma mensagem de erro deve ser exibida para o usuário, indicando tal situação;

* Ler a primeira transação(primeira linha do arquivo) para determinar qual a data das transações desse arquivo em específico;

* Se alguma transação posterior estiver com outra data diferente, ela deve ser ignorada e não ser salva no banco de dados;

* A aplicação não deve "duplicar" transações de um determinado dia, ou seja, se o upload de transações de um determinado dia já tiver sido realizado anteriormente, uma mensagem de erro deve ser exibida ao usuário, indicando que as transações daquela data já foram realizadas;

* Todas as informações da transação são obrigatórias, ou seja, se alguma transação estiver com alguma informação faltando, ela também deve ser ignorada e nao ser salva no banco de dados.

:heavy_check_mark: CRUD de usuários

Para proteger o acesso à aplicação, foi desenvolvida uma interface para gerenciamento dos usuários do sistema. Foi implementado um CRUD de usuários, contendo as telas para cadastrar, editar e excluir um usuário considerando as seguintes regras:

* Para o cadastro, é preciso informar nome e email;

* A aplicação deve gerar uma senha aleatória para o usuário, composta de 6 números;

* A senha deverá ser enviada para o email do usuário sendo cadastrado;

* A senha não deve ser armazenada no banco de dados em texto aberto, devendo ser salvo um hash dela, gerado por um algoritmo de encriptação;

* A aplicação não deve permitir o cadastro de um usuário com o nome ou email de outro usuário já cadastrado, devendo exibir uma mensagem de erro caso essa situação ocorra;

* A aplicação deve ter um usuário padrão previamente cadastrado, com nome: Admin, email: admin@email.com.br;

* O usuário padrão não pode ser editado e nem excluído da aplicação, tampouco deve ser exibido na lista de usuários cadastrados;

* Qualquer usuário tem permissão para listar, cadastrar, alterar e excluir outros usuários;

* Um usuário não pode excluir ele próprio da aplicação.

obs: a aplicação deve considerar o conceito de exclusão lógica, já que para apagar o registro do usuário, seria necessário excluir todo o seu histórico de importações.

:heavy_check_mark: Controle de Acesso

O controle de acesso na aplicação deverá conter uma página de login. A aplicação também deve restringir o acesso à todas as páginas(exceto a página de login) para os usuários que não estejam previamente autenticados. Também deve ser adicionada uma barra de menu na aplicação, contendo os links para as funcionalidades existentes, bem como um botão para o usuário realizar o logout. Esse menu somente deve ser exibido para usuários autenticados.

:heavy_check_mark: Relatório de transações suspeitas

A funcionalidade permite a análise de transações suspeitas. Uma transação deve ser considerada suspeita se o seu valor for igual ou superior a R$100.000,00. Uma conta bancária deve ser considerada suspeita se o somatório de sua movimentação no mês for superior a R$1.000.000,00, seja enviando ou recebendo tal quantia. Uma agência bancária deve ser considerada suspeita se o somatório das movimentações no mês de todas as suas contas for superior a R$1.000.000.000,00, seja enviando ou recebendo tal quantia.

# Tecnologias utilizadas

* Python/Django
* HTML/CSS/Bootstrap
* PostgreSQL

# Acesso ao Projeto

https://transacoesfinanceiras.herokuapp.com/

Usuário: Admin

Senha: alurabackend3
