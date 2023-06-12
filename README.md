# Aratuque

## Descrição

Este projeto é um aplicativo web em Python usando o framework Flask para gerenciar uma biblioteca de músicas, feito para dar suporte ao artefato físico Aratuque. Os usuários podem fazer login, fazer upload de músicas, visualizar sua biblioteca pessoal e reproduzir as músicas carregadas.

## Funcionalidades

1. Autenticação de usuários: os usuários podem fazer login, registrar uma nova conta e fazer logout.
2. Upload de músicas: os usuários podem fazer upload de arquivos de áudio (no formato suportado) para adicionar músicas à sua biblioteca pessoal.
3. Visualização da biblioteca: os usuários podem visualizar todas as músicas que carregaram em sua biblioteca pessoal.
4. Reprodução de músicas: os usuários podem reproduzir as músicas carregadas em seu navegador.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados no seu sistema:

1. Python
2. Flask
3. Flask-Login
4. Werkzeug
5. Flask-SQLAlchemy
6. Flask-Uploads

## Instalação

1. Clone este repositório para o seu sistema.
2. Navegue até o diretório do projeto.
3. Crie um ambiente virtual usando o comando: `python -m venv venv`.
4. Ative o ambiente virtual usando o comando apropriado para o seu sistema operacional.
5. Instale as dependências do projeto usando o comando: `pip install -r requirements.txt`.
6. Configure as variáveis de ambiente necessárias, como `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI` e `UPLOADED_AUDIO_DEST`.
7. Execute o aplicativo com o comando: `python app.py`.

## Uso

1. Acesse o aplicativo em seu navegador: [http://localhost:5000](http://localhost:5000).
2. Na página inicial, você pode fazer login se já tiver uma conta ou registrar uma nova conta.
3. Após fazer login, você será redirecionado para a página da biblioteca, onde poderá ver todas as músicas que carregou.
4. Para adicionar uma nova música, clique no botão "Upload" e preencha os detalhes da música, como título e autor, e selecione um arquivo de áudio para fazer upload.
5. Depois de fazer o upload, a música aparecerá em sua biblioteca pessoal.
6. Você pode clicar no título da música para reproduzi-la em seu navegador.
