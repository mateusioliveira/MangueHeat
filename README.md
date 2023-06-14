# README - Aratuque

## Descrição

Esse projeto é um site de apoio ao artefato físico Aratuque. Usando Python e o framework Flask, ele permite que os usuários se registrem, façam login, saiam e acessem as músicas que produziram no Aratuque.

## Pré-requisitos

- Python (versão 3.6 ou superior)
- Flask (versão 1.1.2 ou superior)
- Flask-Login (versão 0.5.0 ou superior)
- Werkzeug (versão 2.0.1 ou superior)
- SQLite 

## Instalação

1. Clone o repositório ou baixe o código-fonte.
2. Instale “pip install Werkzeug==2.0.1”
3. Instale "pip install flask-login"


## Uso
1. Rode a aplicacao com `python app.py`.
2. Acesse o aplicativo em [http://localhost:5000](http://localhost:5000).

## Funcionalidade

- Pagina inicial: "/"
- Pagina de login: "/login"
- Logout do usuario: "/logout"
- Página de registro do usuário: "/register"
- Acesso a biblioteca de músicas: "/biblioteca"
- Carregar página de arquivo de áudio: "/upload"

O aplicativo usa um banco de dados SQLite chamado "users.db" para armazenar informações do usuário. O banco de dados contém uma tabela de "usuarios" com colunas para ID de usuário, nome de usuário e senha com hash.
