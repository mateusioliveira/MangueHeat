from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, AUDIO
import datetime
import sqlite3
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sua_URI_do_banco_de_dados'
app.config['UPLOADED_AUDIO_DEST'] = 'caminho_para_o_diretorio_de_upload'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
audio_uploads = UploadSet('audio', AUDIO)
configure_uploads(app, audio_uploads)

con = sqlite3.connect("users.db")
cursor = con.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);')
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);')

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
    
    session.clear()
    
    if request.method == 'POST':
        
        username = request.form.get("username")
        senha = request.form.get('senha')
        
        if not username:
            return render_template("login.html", info='Deve fornecer nome de usuário.')
        elif not senha:
            return render_template("login.html", info='Deve fornecer senha.')
        
        colunas = cursor.execute("SELECT * FROM users WHERE username = ?", username)
        
        if len(colunas) != 1 or not check_password_hash(colunas[0]["hash"], senha):
            return render_template("login.html", info='Credenciais inválidas')

        session["user_id"] = colunas[0]["id"]

        return redirect("/")

    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    
    logout_user()
    
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        senha = request.form.get("senha")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template("register.html", info='Deve fornecer nome de usuário.')
        elif not senha:
            return render_template("register.html", info='Deve fornecer senha.')
        elif not confirmation:
            return render_template("register.html", info="Confirme a senha.")

        if senha != confirmation:
            return render_template("register.html", info="Senhas estão diferentes.")

        try:
            hash = generate_password_hash(senha)
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect("/")
        except:
            return render_template("register.html", info="Nome de usuário já existente.")
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
