from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
  
    session.clear()

    if request.method == "POST":
        if not request.form.get("mail"):
            return render_template("login.html", info='Deve fornecer e-mail.')
        elif not request.form.get("password"):
            return render_template("login.html", info='Deve fornecer senha.')

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("mail"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", info='Credenciais inválidas.')

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        mail = request.form.get("mail")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not mail:
            return render_template("register.html", info='Deve fornecer e-mail.')
        elif not password:
            return render_template("register.html", info='Deve fornecer senha.')
        elif not confirmation:
            return render_template("register.html", info="Confirme a senha.")

        if password != confirmation:
            return render_template("register.html", info="Senhas estão diferentes.")

        try:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", mail, hash)
            return redirect("/")
        except:
            return render_template("register.html", info="Endereço de e-mail já usado.")

    else:
        return render_template("register.html")
