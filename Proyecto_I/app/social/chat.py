from flask import request, session, Blueprint, json
from base import *
import sqlalchemy

chat = Blueprint('chat', __name__)



@chat.route('/chat/AElimContacto')
def AElimContacto():
    #GET parameter
    idAmigo = request.args['id']
    idUsuario = session['usuario']['idUsuario']
    
    results = [{
        'label':'/VAdminContactos', 
        'msg':['Contacto eliminado']
        },
        {
        'label':'/VAdminContactos', 
        'msg':['No se pudo eliminar contacto']
    }]
    
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    relacion = sonAmigos(idAmigo,idUsuario)
    print("Relacion",relacion.usuario1,relacion.usuario2,idAmigo,idUsuario)
    if relacion is None:
        res = results[1]
    else:
        db.session.delete(relacion)
        db.session.commit()
        
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AElimMiembro', methods=['POST'])
def AElimMiembro():
    #GET parameter
    params = request.get_json()
    idUsuario = params['idUsuario']
    idGrupo = params['idGrupo']
    
    results = [{'label':'/VGrupo', 'msg':['Miembro eliminado']}, {'label':'/VGrupo', 'msg':['El miembro no pudo ser eliminado']},]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    membresia = Membresia.query.filter_by(idGrupo=idGrupo, idUsuario=idUsuario).first()
    if membresia:
        db.session.delete(membresia)
        db.session.commit()
    else:
        res = results[1]
    
    res['label'] = res['label'] + '/' + idGrupo

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AEscribir', methods=['POST'])
def AEscribir():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VChat', 'msg':['Enviado']}, {'label':'/VChat', 'msg':['No se pudo enviar mensaje']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + repr(1)


    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/ASalirGrupo', methods=['POST'])
def ASalirGrupo():
    #POST/PUT parameters
    params = request.get_json()
    idGrupo = params['idGrupo']
    idUsuario = session['usuario']['idUsuario']
    results = [{'label':'/VAdminContactos', 'msg':['Ya no estás en ese grupo']}, {'label':'/VGrupo', 'msg':['No puedes salir del grupo']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    membresia = Membresia.query.filter_by(idUsuario=idUsuario, idGrupo=idGrupo).first()
    if membresia:
        db.session.delete(membresia)
        if membresia.es_admin:
            nuevoAdmin = Membresia.query.filter_by(idGrupo = idGrupo).first()
            if nuevoAdmin:
                nuevoAdmin.es_admin = True
                db.session.add(nuevoAdmin)
                res['label'] = res['label'] + '/' + idGrupo
            else:
                res = results[1]
        else:
            res['label'] = res['label'] + '/' + idGrupo
        db.session.commit()


    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AgregContacto', methods=['POST'])
def AgregContacto():
    #POST/PUT parameters
    params = request.get_json()
    idAmigo = params['id']
    idUsuario = session['usuario']['idUsuario']
    
    results = [
        {
            'label':'/VAdminContactos', 
            'msg':['Contacto agregado']
        }, 
        {
            'label':'/VAdminContactos',
            'msg':['No se pudo agregar contacto']
        }
    ]
    
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    
    try:
        relacion = Contacto(usuario1=idUsuario,usuario2=idAmigo)
        db.session.add(relacion)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        print("Hice rollback")
        res = results[1]
    

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)

@chat.route('/chat/AgregGrupo', methods=['POST'])
def AgregGrupo():
    params = request.get_json()
    print(params)
    nombreGrupo = params['nombre']
    results = [{'label':'/VAdminContactos', 'msg':['Grupo agregado']}, {'label':'/VAdminContactos', 'msg':['Error al crear grupo']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    if 'usuario' in session:
        grupo = Grupo(nombre=nombreGrupo)
        db.session.add(grupo)
        db.session.commit()
        res['idGrupo'] = grupo.idGrupo
        membresia = Membresia(
            idUsuario=session['usuario']['idUsuario'],
            idGrupo=grupo.idGrupo,
            es_admin=True
        )
        db.session.add(membresia)
        db.session.commit()
    else:
        res = results[1]

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)


@chat.route('/chat/AgregMiembro', methods=['POST'])
def AgregMiembro():
    #POST/PUT parameters
    params = request.get_json()
    idGrupo = params['idGrupo']
    idUsuario = params['idUsuario']
    results = [{'label':'/VGrupo', 'msg':['Nuevo miembro agregado']}, {'label':'/VGrupo', 'msg':['No se pudo agregar al nuevo miembro']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    grupo = Grupo.query.filter_by(idGrupo=idGrupo)
    usuario = Usuario.query.filter_by(idUsuario=idUsuario)
    
    if grupo and usuario:
        try:
            membresia = Membresia(idUsuario=idUsuario, idGrupo=idGrupo, es_admin=False)
            db.session.add(membresia)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            print("Hice rollback")
            res = results[1]
    else:
        res = results[1]
        
    res['label'] = res['label'] + '/' + idGrupo


    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/VAdminContactos')
def VAdminContactos():
    #GET parameter
    idUsuario = session['usuario']['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    contactos = obtenerAmigos(idUsuario)
    res['contactos'] = [
        {
          'idContacto':contacto.idUsuario, 
          'nombre':contacto.nombre, 
          'tipo':'usuario'
        } for contacto in contactos
    ]
    grupos = obtenerGrupos(idUsuario)
    res['grupos'] = [
        {
          'idContacto':grupo.idGrupo, 
          'nombre':grupo.nombre, 
          'tipo':'grupo'
        } for grupo in grupos
    ]

    res['idGrupo'] = 1
    res['fContacto_opcionesNombre'] = [
        {
          'key':usuario.idUsuario,
          'value':usuario.nombre
        } for usuario in Usuario.query.filter(Usuario.idUsuario != idUsuario).all()
    ]

    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VChat')
def VChat():
    #GET parameter
    idChat = request.args['idChat']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure



    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VContactos')
def VContactos():
    #GET parameter
    idUsuario = session['usuario']['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['contactos'] = [
        {
          'idContacto':contacto.idUsuario,
          'nombre':contacto.nombre, 
          'tipo':'usuario'
        } for contacto in obtenerAmigos(idUsuario)
    ]
    res['grupos'] = [
        {
            'idContacto': grupo.idGrupo,
            'nombre': grupo.nombre,
            'tipo': 'grupo'
        } for grupo in obtenerGrupos(idUsuario)
    ]

    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VGrupo')
def VGrupo():
    #GET parameter
    idGrupo = request.args['idGrupo']
    idUsuario = session['usuario']['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    
    contactos = obtenerAmigos(idUsuario)
   
    res['idGrupo'] = idGrupo
    res['fMiembro_opcionesNombre'] = [
        {
          'key':contacto.idUsuario,
          'value':contacto.nombre
        } for contacto in contactos
    ]
    res['data3'] = [
        {
          'idContacto':contacto.idUsuario,
          'nombre': Usuario.query.filter_by(idUsuario=contacto.idUsuario).first().nombre,
          'tipo': "usuario"
        } for contacto in Grupo.query.filter(Grupo.idGrupo == idGrupo).first().usuarios
    ]

    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here

