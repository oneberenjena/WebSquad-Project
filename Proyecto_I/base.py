from flask import Flask, session
from flask.ext.script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send, join_room
from random import SystemRandom
from datetime import timedelta
from datetime import datetime

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

    #Relacionando con las publicaciones
    publicaciones = db.relationship('Publicacion', backref="usuario", cascade="all, delete-orphan" , lazy='dynamic')
    
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

class Grupo(db.Model):
    idGrupo = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    usuarios = db.relationship("Membresia")

class Membresia(db.Model):
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), primary_key=True)
    idGrupo = db.Column(db.Integer, db.ForeignKey('grupo.idGrupo'), primary_key=True)
    es_admin = db.Column(db.Boolean)
    usuario = db.relationship("Usuario")


# para la relacion recursiva
# http://stackoverflow.com/questions/20830147/unable-to-create-self-referencing-foreign-key-in-flask-sqlalchemy
class Publicacion(db.Model):
    __tablename__ = 'publicacion'
    idPublicacion = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50), nullable = False)
    contenido = db.Column(db.Text, nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    
    # Relacion con el usuario
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable = False)
    # autor = db.relationship('Usuario', backref = db.backref('publicacion', lazy = 'dynamic'))
    
    # Relacion recursiva publicacion raiz
    padre_id = db.Column(db.Integer, db.ForeignKey('publicacion.idPublicacion'), nullable=True)
    
    hilo_id = db.Column(db.Integer, db.ForeignKey('hilo.idHilo'), nullable=True)
    
    # SIENTO QUE FALTA ALGO AQUI PARA LA RELACION RECURSIVA

    def __init__(self, titulo, contenido, autor_id, tipo, padre_id = None, foro_id = None, pag_id = None, fecha = None):
        self.titulo = titulo
        self.contenido = contenido
        
        if fecha is None:
            fecha = datetime.utcnow()
        self.fecha = fecha
        
        self.autor_id = autor_id
        self.padre_id = padre_id


    def __rep__(self):
        return '<titulo de la publicacion: {} \ncontenido: {} son amigos'.format(self.titulo, self.contenido)
        
        
#http://stackoverflow.com/questions/22976445/flask-sqlalchemy-how-do-i-declare-a-base-class
#http://techarena51.com/index.php/one-to-many-relationships-with-flask-sqlalchemy/
class Hilo(db.Model):
    __tablename__ = 'hilo'
    idHilo = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50), nullable = False)
    
    # Relacion con la publicacion raiz
    pubRaiz_id = db.Column(db.Integer, db.ForeignKey('publicacion.idPublicacion'), nullable = False)
    pubRaiz = db.relationship('Publicacion', backref = db.backref('publicacion_Raiz', uselist=False), foreign_keys = [pubRaiz_id])
    
    publicaciones = db.relationship('Publicacion', backref=db.backref('hilo'), foreign_keys=[Publicacion.hilo_id])
    # Para identificar si es un hilo de foro o uno de una pagina comentable si es 1 es de foro y 0 de pag
    tipo = db.Column(db.Integer, nullable = False)
    foro_id = db.Column(db.Integer, db.ForeignKey('foro.idForo'), nullable=True)
    pag_id = db.Column(db.Integer, db.ForeignKey('paginaSitio.idPagSitio'), nullable = True)
    
    
    
        
class Foro (db.Model):
    idForo = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50), nullable = False, unique = True)
    fecha_creacion = db.Column(db.DateTime, nullable = False)
    
    # relacion con el usuario
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable = False)
    autor = db.relationship('Usuario', backref = db.backref('foro', lazy = 'dynamic'))
    
    # Relacion con los hilos
    hilos = db.relationship('Hilo', backref='foro', cascade="all, delete-orphan")
    
    def __init__(self, titulo, autor, fecha = None):
        self.titulo = titulo
        self.autor_id = autor
        if fecha is None:
            fecha = datetime.utcnow()
        self.fecha_creacion = fecha
        
    def __rep__(self):
        return '<Foro %r>' % self.titulo
        
class PaginaSitio(db.Model):
    __tablename__ = 'paginaSitio'
    idPagSitio = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(80), unique = True, nullable = False)
    
    # Relacion con hilos
    hilos = db.relationship('Hilo', backref='pagSitio', cascade="all, delete-orphan", lazy='dynamic')
    


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

def obtenerGrupos(idUsuario):
    return Membresia.query.join(Grupo, Grupo.idGrupo == Membresia.idGrupo).add_columns(
        Grupo.idGrupo, Grupo.nombre).filter(Membresia.idUsuario==idUsuario).all()
#Application code ends here

from app.social.ident import ident
app.register_blueprint(ident)
from app.social.paginas import paginas
app.register_blueprint(paginas)
from app.social.chat import chat
app.register_blueprint(chat)
from app.social.foro import foro
app.register_blueprint(foro)

@socketio.on('message')
def message_handler(data):
    message = {
        'msg':data['msg'], 
        'room': data['idChat'],
        'idUsuario': session['usuario']['idUsuario'] if 'usuario' in session else 0
    }
    send(message=message, room=data['idChat'])
    print(data['msg'])
    return room

@socketio.on('connect')
def connect_handler():
    print("conectar")
    if 'usuario' in session:
        room = "usuario_{}".format(session['usuario']['idUsuario'])
        join_room(room)
        for grupo in obtenerGrupos(session['usuario']['idUsuario']):
            join_room("grupo_" + str(grupo.idGrupo))
            
        print("Conectado y en el room " + room)
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
    socketio.run(app, host='0.0.0.0',port=8080,debug=True)