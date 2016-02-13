from flask import Flask, session
from flask.ext.script import Manager, Server
from random import SystemRandom
from datetime import timedelta

app = Flask(__name__, static_url_path='')
manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0', port = 8080)
)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=45)
    session.modified = True

from flask_SQLAlchemy import SQLAlchemy

@app.route('/')
def root():
    return app.send_static_file('index.html')

#Application code starts heres
    db = SQLAlchemy(app)

    class Usuario(db.Model):
        id_Usuario = db.Column(db.Integer, primay_key = True)
        nombre = db.Column(db.String(20), nullable = False)
        user_Name = db.Column(db.String(10), index = True, unique = True, nullable = False)
        contrasena = db.Column(db.Sting(15), nullable = False)
        correo = db.Column(db.Sting(80), unique = True, nullable = False)
        # pagina_id = db.Column(db.Integer, db.ForeignKey('Pagina.id_Pagina'))
        
        def __init__(self, nombre, user_Name, contrasena, correo):
            self.nombre = nombre
            user_Name = user_Name
            contrasena = contrasena
            correo = correo
            
    class Pagina(db.Model):
        id_Pagina = db.Column(db.Integer, primay_key = True)
        titulo = db.Column(db.Sting(50), nullable = True)
        contenido = db.Column(db.Text, nullable = True)
        usuario = db.relationship('Usuario',backref = db.backref('pagina'), lazy = 'dynamic')
        
        def __init__(seld, titulo, contenido, usuario):
            self.titulo = titulo
            self.contenido = contenido
            self.usuario = usuario

#Application code ends here

from app.socal.ident import ident
app.register_blueprint(ident)
from app.socal.paginas import paginas
app.register_blueprint(paginas)


if __name__ == '__main__':
    app.config.update(
      SECRET_KEY = repr(SystemRandom().random())
    )
    manager.run()

