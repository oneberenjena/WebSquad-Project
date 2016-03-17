from flask import Flask, session
from flask.ext.script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send, join_room
from random import SystemRandom
from datetime import timedelta

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

socketio = SocketIO(app, engineio_logger=True)

# Llevar seguimiento del id del socket de cada usuario
clients = []

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    idPagina = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50), nullable = True)
    contenido = db.Column(db.Text, nullable = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    usuario = db.relationship('Usuario', backref = db.backref('paginas', lazy = 'dynamic'))
    
    
    def __rep__(self):
        return '<Pagina %r>' % self.titulo

class Contacto(db.Model):
    __tablename__ = 'contacto'
    idContacto = db.Column(db.Integer, primary_key=True)
    usuario1 = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    usuario2 = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    __table_args__ = (db.UniqueConstraint('usuario1', 'usuario2', name='_amistad'),)
    
    def __rep__(self):
        return '<{} y {} son amigos'.format(self.usuario1, self.usuario2)

def sonAmigos(id1,id2):
    relacion1 = Contacto.query.filter_by(usuario1=id1,usuario2=id2).first()
    relacion2 = Contacto.query.filter_by(usuario1=id2, usuario2=id1).first()
    relacion = relacion1 if relacion2 is None else relacion2
    return relacion

def obtenerAmigos(idUsuario):
    c1 = Contacto.query.join(
        Usuario, Contacto.usuario2 == Usuario.idUsuario
    ).add_columns(
        Usuario.nombre,Usuario.idUsuario, Contacto.idContacto
    ).filter(Contacto.usuario1==idUsuario).all()
    
    c2 = Contacto.query.join(
        Usuario, Contacto.usuario1 == Usuario.idUsuario
    ).add_columns(
        Usuario.nombre,Usuario.idUsuario, Contacto.idContacto
    ).filter(Contacto.usuario2==idUsuario).all()
    
    return c1 + c2
        
#Application code ends here

from app.social.ident import ident
app.register_blueprint(ident)
from app.social.paginas import paginas
app.register_blueprint(paginas)
from app.social.chat import chat
app.register_blueprint(chat)

@socketio.on('message')
def message_handler(data):
    send(message=data['msg'], room='{}_{}'.format(data['tipo'],data['idUsuario']))
    print(data['msg'])

@socketio.on('connect')
def connect_handler():
    print("conectar")
    if 'usuario' in session:
        room = "usuario_{}".format(session['usuario']['idUsuario'])
        join_room(room)
        print("Conectado y en el room")
    else:
        print("Conectado")

@socketio.on('join')
def join_room_handler(data):
    print("Joining")
    room = "{}_{}".format(data['tipo'],data['room'])
    join_room(room)

@socketio.on_error_default
def chat_error_handler(e):
    print('An error has occurred: ' + str(e),e)

if __name__ == '__main__':
    app.config.update(
      SECRET_KEY = repr(SystemRandom().random())
    )
    #manager.run()
    socketio.run(app, host='0.0.0.0',port=8080)