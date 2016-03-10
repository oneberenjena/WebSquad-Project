from flask import Flask, session
from flask.ext.script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from random import SystemRandom
from datetime import timedelta

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0', port = 8080)
)
manager.add_command('db', MigrateCommand)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=45)
    session.modified = True

@app.route('/')
def root():
    return app.send_static_file('index.html')

#Application code starts heres

class Usuario(db.Model):
    idUsuario = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(15), index = True, unique = True, nullable = False)
    contrasena = db.Column(db.String(16), nullable = False)
    correo = db.Column(db.String(80), unique = True, nullable = False)
    #pagina_id = db.Column(db.Integer, db.ForeignKey('Pagina.id_Pagina'), nullable = True)
    
    def __init__(self, nombre, username, contrasena, correo):
        self.nombre = nombre
        self.username = username
        self.contrasena = contrasena
        self.correo = correo
        
    def __rep__(self):
        return '<Usuario %r>' % self.nombre
        
class Pagina(db.Model):
    id_Pagina = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50), nullable = True)
    contenido = db.Column(db.Text, nullable = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    usuario = db.relationship('Usuario', backref = db.backref('paginas', lazy = 'dynamic'))
    
    
    def __rep__(self):
        return '<Pagina %r>' % self.titulo

#Application code ends here

from app.social.ident import ident
app.register_blueprint(ident)
from app.social.paginas import paginas
app.register_blueprint(paginas)
from app.socal.chat import chat
app.register_blueprint(chat)


if __name__ == '__main__':
    app.config.update(
      SECRET_KEY = repr(SystemRandom().random())
    )
    manager.run()

