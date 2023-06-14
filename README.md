# README - Aratuque

## Flask Autenticação do Usuário

Este é um aplicativo Flask que fornece funcionalidade de autenticação do usuário usando SQLite para armazenamento de dados e gerenciamento de sessão do Flask para login do usuário. Ele permite que os usuários se registrem, façam login, saiam e acessem rotas protegidas.

## Pré-requisitos

- Python (versão 3.6 ou superior)
- Flask (versão 1.1.2 ou superior)
- Flask-Login (versão 0.5.0 ou superior)
- Werkzeug (versão 2.0.1 ou superior)
- SQLite (integrado ao Python)

## Instalação

1. Clone o repositório ou baixe o código-fonte.
2. Instale as dependências necessárias com `pip install -r requirements.txt`.


## Uso
1. Rode a aplicacao com `python app.py`.
2. Acesse o aplicativo em [http://localhost:5000](http://localhost:5000).

## Funcionalidade

- Pagina inicial: "/"
- Pagina de login: "/login"
- Logout do usuario: "/logout"
- Página de registro do usuário: "/register"
- Rota protegida (requer autenticação): "/biblioteca"
- Carregar página de arquivo de áudio (rota protegida): "/upload"

O aplicativo usa um banco de dados SQLite chamado "users.db" para armazenar informações do usuário. O banco de dados contém uma tabela de "usuarios" com colunas para ID de usuário, nome de usuário e senha com hash.
