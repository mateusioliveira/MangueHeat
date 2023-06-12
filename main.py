from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, AUDIO
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sua_URI_do_banco_de_dados'
app.config['UPLOADED_AUDIO_DEST'] = 'caminho_para_o_diretorio_de_upload'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
audio_uploads = UploadSet('audio', AUDIO)
configure_uploads(app, audio_uploads)

# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)

class Musica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('musicas', lazy=True))

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        
        if not nome_usuario:
            return render_template("login.html", info='Deve fornecer nome de Usuário.')
        elif not senha:
            return render_template("login.html", info='Deve fornecer senha.')
        
        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for('biblioteca'))
        if not usuario or not check_password_hash(usuario.senha, senha):
            return render_template('login.html', info='E-mail ou senha inválidos.')
        # Realiza o login do usuário
        else:
            return 'Nome de usuário ou senha inválidos'

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        nome_usuario = request.form.get("nome_usuario")
        senha = request.form.get("senha")
        confirmation = request.form.get("confirmation")

        if not nome_usuario:
            return render_template("register.html", info='Deve fornecer Nome de Usuário.')
        elif not senha:
            return render_template("register.html", info='Deve fornecer senha.')
        elif not confirmation:
            return render_template("register.html", info="Confirme a senha.")

        if senha != confirmation:
            return render_template("register.html", info="Senhas estão diferentes.")

        try:
            hash = generate_password_hash(senha)
            db.session.add("INSERT INTO users (username, hash) VALUES (?, ?)", nome_usuario, hash)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return render_template("register.html", info="Nome de Usuário já usado.")
    else:
        return render_template("register.html")

@app.route('/biblioteca')
@login_required
def biblioteca():
    musicas_usuario = current_user.musicas
    return render_template('biblioteca.html', musicas=musicas_usuario)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        audio = request.files['audio']
        filename = audio_uploads.save(audio)
        titulo = request.form['titulo']
        autor = request.form['autor']
        musica = Musica(titulo=titulo, autor=autor, usuario=current_user)
        db.session.add(musica)
        db.session.commit()
        return redirect(url_for('biblioteca'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
