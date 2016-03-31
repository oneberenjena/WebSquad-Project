from flask import request, session, Blueprint, json, jsonify
from base import *
import sqlalchemy
from sqlalchemy.ext.serializer import loads, dumps

chat = Blueprint('chat', __name__)

@chat.route('/chat/AElimContacto', methods=['POST'])
def AElimContacto():
    #GET parameter
    params = request.get_json()
    idAmigo = params['idAmigo']

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

    contacto = Contacto.query.filter_by(idContacto=idAmigo).first()

    contactos = [
        {
            "id": contacto.idContacto,
            "usuario1": contacto.usuario1,
            "usuario2": contacto.usuario2
        } for contacto in Contacto.query.all()
    ]

    #Action code goes here, res should be a list with a label and a message

    if contacto is None:
        res = results[1]
    else:
        db.session.delete(contacto)
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
    
    res['label'] = res['label'] + '/' + str(idGrupo)

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
    grupo = Grupo.query.filter_by(idGrupo=idGrupo).first()

    if membresia:
        db.session.delete(membresia)
        if membresia.es_admin:
            nuevoAdmin = Membresia.query.filter_by(idGrupo = idGrupo).first()
            if nuevoAdmin:
                nuevoAdmin.es_admin = True
                db.session.add(nuevoAdmin)
                res['label'] = res['label'] + '/' + idGrupo
            else:
                db.session.delete(grupo)
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
    #GET parameter
    params = request.get_json()
    nombreGrupo = params['nombre']
    results = [{'label':'/VAdminContactos', 'msg':['Grupo agregado']}, {'label':'/VAdminContactos', 'msg':['Error al crear grupo']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    if 'usuario' in session:
        grupo = Grupo(nombre=nombreGrupo)
        db.session.add(grupo)
        db.session.commit()
        
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
    res['data1'] = [
        {
          'idContacto':contacto.idUsuario, 
          'nombre':contacto.nombre, 
          'tipo':'usuario'
        } for contacto in contactos
    ]
    grupos = obtenerGrupos(idUsuario)
    res['data2'] = [
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

    res['data1'] = [
        {
          'idContacto':contacto.idUsuario,
          'nombre':contacto.nombre, 
          'tipo':'usuario'
        } for contacto in obtenerAmigos(idUsuario)
    ]
    res['data1'] += [
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




























# PARTE ARREGLADA

@chat.route('/api/users/list')
def listUsers():
    correo = request.args['correo']

    usuarios = Usuario.query.filter_by(correo=correo).all()

    usuarios = [
        {
          'idUsuario':usuario.idUsuario,
          'nombre': usuario.nombre,
          'correo': usuario.correo
        } for usuario in usuarios
    ]

    return json.dumps(usuarios)

# CONTACTOS

@chat.route('/api/contacts/create', methods=['POST'])
def createContact():
    #POST/PUT parameters
    params = request.get_json()
    idAmigo = params['idUsuario']
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
    

    # #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    
    return json.dumps(res)

@chat.route('/api/contacts/list')
def listContacts():
    #GET parameter
    idUsuario = session['usuario']['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']

    res['data1'] = [
        {
          'idUsuario':contacto.idUsuario,
          'idContacto':contacto.idContacto,
          'nombre':contacto.nombre,
          'tipo':'usuario'
        } for contacto in obtenerAmigos(idUsuario)
    ]

    # res['data1'] += [
    #     {
    #         'idContacto': grupo.idGrupo,
    #         'nombre': grupo.nombre,
    #         'tipo': 'grupo'
    #     } for grupo in obtenerGrupos(idUsuario)
    # ]

    #Action code ends here
    return json.dumps(res)

@chat.route('/api/contacts/remove/<int:id>', methods=['DELETE'])
def removeContact(id):
    #GET parameter
    idContacto = id

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

    contacto = Contacto.query.filter_by(idContacto=idContacto).first()

    #Action code goes here, res should be a list with a label and a message

    if contacto is None:
        res = results[1]
    else:
        db.session.delete(contacto)
        db.session.commit()
        
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps([])



# 
# GRUPOS
# 


@chat.route('/api/groups/create', methods=['POST'])
def createGroup():
    #GET parameter
    params = request.get_json()
    nombreGrupo = params['nombre']
    results = [{'label':'/VAdminContactos', 'msg':['Grupo agregado']}, {'label':'/VAdminContactos', 'msg':['Error al crear grupo']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    grupo = Grupo(nombre=nombreGrupo)
    
    if 'usuario' in session:
        db.session.add(grupo)
        db.session.commit()
        
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

    return json.dumps(grupo.idGrupo)

@chat.route('/api/groups/list')
def listGroups():
    grupos = Grupo.query.all()

    grupos = [
        {
          'idGrupo':grupo.idGrupo,
          'nombre': grupo.nombre
        } for grupo in grupos
    ]

    return json.dumps(grupos)

@chat.route('/api/groups/show/<int:id>')
def showGroup(id):
    grupo = Grupo.query.filter_by(idGrupo=id).first()

    grupo = {
        'idGrupo': grupo.idGrupo,
        'nombre': grupo.nombre
    }

    return json.dumps(grupo)

@chat.route('/api/groups/remove/<int:id>', methods=['DELETE'])
def deleteGroup(id):
    #GET parameter
    #print (Membresia.query.filter_by(idMembresia = id).first())
    idGrupo = id
    
    results = [{'label':'/VGrupo', 'msg':['Miembro eliminado']}, {'label':'/VGrupo', 'msg':['El miembro no pudo ser eliminado']},]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    grupo = Grupo.query.filter_by(idGrupo=idGrupo).first()
    if grupo:
        db.session.delete(grupo)
        db.session.commit()
    else:
        res = results[1]
    
    res['label'] = res['label'] + '/' + str(idGrupo)

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)


# 
# MEMBRESIA
# 

@chat.route('/api/memberships/create', methods=['POST'])
def createMembership():
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

@chat.route('/api/memberships/list')
def listMemberships():
    #GET parameter
    idUsuario = session['usuario']['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']

    res['data1'] = [
        {
          'id': membresia.idMembresia,
          'usuario': membresia.idUsuario,
          'grupo': membresia.idGrupo,
          'es_admin': membresia.es_admin,
        } for membresia in Membresia.query.all()
    ]

    #Action code ends here
    return json.dumps(res)

@chat.route('/api/memberships/remove/<int:id>', methods=['DELETE'])
def deleteMembership(id):
    #GET parameter
    #print (Membresia.query.filter_by(idMembresia = id).first())
    idMembresia = id
    
    results = [{'label':'/VGrupo', 'msg':['Miembro eliminado']}, {'label':'/VGrupo', 'msg':['El miembro no pudo ser eliminado']},]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    membresia = Membresia.query.filter_by(idMembresia=idMembresia).first()
    if membresia:
        db.session.delete(membresia)
        db.session.commit()
    else:
        res = results[1]
    
    res['label'] = res['label'] + '/' + str(idMembresia)

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)