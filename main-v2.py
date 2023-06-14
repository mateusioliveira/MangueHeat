from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user
import sqlite3
import os

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'mangueHeat'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    con = sqlite3.connect("users.db")
    cursor = con.cursor()
    colunas = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    coluna = colunas.fetchone()

    if coluna:
        user = User(id=coluna[0], username=coluna[1])
        return user

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        username = request.form.get("username")
        senha = request.form.get('senha')

        if not username:
            return render_template("login.html", info='Deve fornecer nome de usuário.')
        elif not senha:
            return render_template("login.html", info='Deve fornecer senha.')

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        coluna = cursor.fetchone()

        if not coluna or not check_password_hash(coluna[2], senha):
            return render_template("login.html", info='Credenciais inválidas')

        user = User(id=coluna[0], username=coluna[1])
        login_user(user)

        return redirect(url_for("index"))

    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
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

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        coluna = cursor.fetchone()

        if coluna is not None:
            return render_template("register.html", info="Nome de usuário já existe.")

        try:
            hash = generate_password_hash(senha)
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
            con.commit()
            return redirect(url_for("login"))
        except:
            return render_template("register.html", info="Erro ao criar usuário.")

    else:
        return render_template("register.html")

@app.route('/biblioteca')
@login_required
def biblioteca():
    return render_template('biblioteca.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'audio' in request.files:

        return redirect(url_for('biblioteca'))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
