from flask import request, session, Blueprint, json
from base import *

import sqlalchemy
chat = Blueprint('chat', __name__)


@socketio.on('message')
def message_handler(data):
    print(data)
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
    print("Relacion",relacion,idAmigo,idUsuario)
    if relacion is None:
        res = results[1]
    else:
        db.session.delete(relacion)
        db.session.commit()
    
    res['label'] = res['label'] + '/' + str(idUsuario)

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AElimMiembro')
def AElimMiembro():
    #GET parameter
    id = request.args['id']
    results = [{'label':'/VGrupo', 'msg':['Miembro eliminado']}, ]
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



@chat.route('/chat/ASalirGrupo')
def ASalirGrupo():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VAdminContactos', 'msg':['Ya no estás en ese grupo']}, {'label':'/VGrupo', 'msg':['Sigues en el grupo']}, ]
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
    
    res['label'] = res['label'] + '/' + str(idUsuario)
    
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
    results = [{'label':'/VGrupo', 'msg':['Nuevo miembro agregado']}, {'label':'/VGrupo', 'msg':['No se pudo agregar al nuevo miembro']}, ]
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



@chat.route('/chat/VAdminContactos')
def VAdminContactos():
    #GET parameter
    idUsuario = session['usuario']['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idContacto'] = 1
    contactos = obtenerAmigos(idUsuario)
    res['data1'] = [
        {
          'idContacto':contacto.idContacto, 
          'nombre':contacto.nombre, 
          'tipo':'usuario'
        } for contacto in contactos
    ]
    res['data2'] = [
      {'idContacto':56, 'nombre':'Grupo Est. Leng.', 'tipo':'grupo'},
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

    res['idChat'] = 1
    res['idUsuario'] = 1
    res['mensajesAnt'] = [
      {'texto': '¿Me traes mi gato por la tarde?', 'usuario':'ana', 'fecha':'lun feb 29 09:08:17 VET 2016'},
      {'texto': '¡Hay! no lo encuentro, debió escaparse. Ahora salgo a buscarlo', 'usuario':'distra', 'fecha':'lun feb 29 09:09:17 VET 2016'},
      {'texto': 'Hola vane, ayer al pasar por tu casa dejé a naco mi anacondita..', 'usuario':'uri', 'fecha':'lun feb 29 09:09:17 VET 2016'},
      {'texto': 'La dejasete fue en mi casa. No la había visto porque está en un rincon, no se mueve y ... pareceira que tiene algo atragantado.', 'usuario':'distra', 'fecha':'lun feb 29 09:10:17 VET 2016'},
      {'texto': '¿Qué?', 'usuario':'ana', 'fecha':'lun feb 29 09:12:17 VET 2016'},
    ]

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

    res['idContacto'] = 1
    contactos = obtenerAmigos(idUsuario)
    print(contactos)
    res['data1'] = [
        {
          'idContacto':contacto.idContacto, 
          'nombre':contacto.nombre, 
          'tipo':'usuario'
        } for contacto in contactos
    ]


    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VGrupo')
def VGrupo():
    #GET parameter
    idGrupo = request.args['idGrupo']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idGrupo'] = 1
    res['fMiembro_opcionesNombre'] = [
      {'key':1, 'value':'Leo'},
      {'key':2, 'value':'Lauri'},
      {'key':3, 'value':'Mara'},
    ]
    res['data3'] = [
      {'idContacto':34, 'nombre':'ana', 'tipo':'usuario'},
      {'idContacto':23, 'nombre':'leo', 'tipo':'usuario'},
      {'idContacto':11, 'nombre':'distra', 'tipo':'usuario'},
      {'idContacto':40, 'nombre':'vane', 'tipo':'usuario'},
    ]

    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here

