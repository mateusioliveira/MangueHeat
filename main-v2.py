from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required
import sqlite3


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

con = sqlite3.connect("users.db")
cursor = con.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);')
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);')

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

        colunas = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        coluna = colunas.fetchone()

        if not coluna or not check_password_hash(coluna[2], senha):
            return render_template("login.html", info='Credenciais inválidas')

        session["user_id"] = coluna[0]

        return redirect("/")

    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
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
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
            con.commit()
            return redirect("/")
        except:
            return render_template("register.html", info="Nome de usuário já existe.")
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
