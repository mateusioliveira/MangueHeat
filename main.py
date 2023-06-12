from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, AUDIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sua_URI_do_banco_de_dados'
app.config['UPLOADED_AUDIO_DEST'] = 'caminho_para_o_diretorio_de_upload'


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
