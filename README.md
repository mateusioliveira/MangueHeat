# Sistema de Registro e Login

Este é um simples sistema de registro e login implementado em Python, utilizando arquivos CSV para armazenar as informações dos usuários.

## Funcionalidades

O sistema possui duas principais funcionalidades:

1. Registro de Usuário: Permite que um novo usuário se registre no sistema fornecendo seu nome, email e senha. Os dados são armazenados em um arquivo CSV chamado `users.csv`.

2. Login de Usuário: Permite que um usuário registrado faça o login fornecendo seu email e senha. O sistema verifica as credenciais inseridas comparando-as com os registros no arquivo CSV.

## Requisitos

- Python 3.x
- Biblioteca CSV (já inclusa na biblioteca padrão do Python)

## Como Executar

1. Clone o repositório ou faça o download dos arquivos.
2. Certifique-se de ter o Python instalado em seu sistema.
3. Execute o código em um ambiente Python compatível.

## Uso

### Registro de Usuário

1. Execute o programa.
2. Digite seu nome, email e senha quando solicitado.
3. As informações serão armazenadas no arquivo `users.csv`.
4. Você receberá uma mensagem de confirmação quando o registro for concluído com sucesso.

### Login de Usuário

1. Execute o programa.
2. Digite seu email e senha quando solicitado.
3. O sistema verificará as informações inseridas com as registradas no arquivo `users.csv`.
4. Se as credenciais estiverem corretas, você receberá uma mensagem de login bem-sucedido.
5. Caso contrário, você receberá uma mensagem informando que o email ou senha está incorreto.

# Aplicativo de Biblioteca de Música

Este é um aplicativo Flask para uma biblioteca de música onde os usuários podem fazer upload de músicas e visualizar sua biblioteca pessoal. O aplicativo usa SQLAlchemy para interagir com o banco de dados e o Flask-Uploads para gerenciar o upload de arquivos de áudio.

## Configuração

Antes de executar o aplicativo, certifique-se de configurar as seguintes variáveis de configuração no arquivo `app.py`:

1. `SECRET_KEY`: Uma chave secreta para a sessão do Flask.
2. `SQLALCHEMY_DATABASE_URI`: A URI do banco de dados que será usado para armazenar os dados.
3. `UPLOADED_AUDIO_DEST`: O caminho para o diretório onde os arquivos de áudio serão salvos.

## Modelos

O aplicativo possui dois modelos de banco de dados:

### `Usuario`

1. `id`: Chave primária do usuário.
2. `nome_usuario`: Nome de usuário do usuário.
3. `senha`: Senha do usuário.

### `Musica`

1. `id`: Chave primária da música.
2. `titulo`: Título da música.
3. `autor`: Autor da música.
4. `data_criacao`: Data de criação da música (preenchida automaticamente com a data e hora atuais).
5. `usuario_id`: Chave estrangeira para o `id` do usuário que enviou a música.
6. `usuario`: Relacionamento com o modelo `Usuario` para obter informações do usuário associado à música.

## Rotas

O aplicativo possui as seguintes rotas:

### `/biblioteca`

1. Descrição: Rota para visualizar a biblioteca de músicas do usuário logado.
2. Método: GET
3. Restrições: O usuário deve estar logado.
4. Função: `biblioteca()`

### `/upload`

1. Descrição: Rota para fazer upload de uma nova música.
2. Método: GET, POST
3. Restrições: O usuário deve estar logado.
4. Função: `upload()`
