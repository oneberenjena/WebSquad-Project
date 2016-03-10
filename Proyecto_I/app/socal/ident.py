from flask import request, session, Blueprint, json

ident = Blueprint('ident', __name__)

from base import db, Usuario, Pagina


@ident.route('/ident/AIdentificar', methods=['POST'])
def AIdentificar():
    #POST/PUT parameters
    params = request.get_json()
    results = [
        {
            'label':'/VPrincipal',
            'msg':['Bienvenido usuario'],
            "actor":"duenoProducto"
        },
        {
            'label':'/VLogin',
            'msg': ['Datos de identificación incorrectos']
        }]
    user = Usuario.query.filter_by(username=params['usuario'],
                                contrasena=params['clave']).first()
    if user:
        res = results[0]
        session['usuario'] = {
            'idUsuario': user.idUsuario,
            'nombre': user.nombre
        }
        session['actor'] = res['actor']
    else:
        res = results[1]
        session.pop("usuario", None)
        session.pop("actor", None)
            
    return json.dumps(res)



@ident.route('/ident/ARegistrar', methods=['POST'])
def ARegistrar():
    #POST/PUT parameters
    params = request.get_json()
    results = [
        {
            'label':'/VLogin',
            'msg':['Felicitaciones, Ya estás registrado en la aplicación']
        },
        {
            'label':'/VRegistro',
            'msg':['Error al tratar de registrarse']
        }
    ]
    
    if not (params['usuario'] and params['correo'] and params['nombre'] and params['clave']):
        res = results[1]
    else:
        try:
            user = Usuario(params['nombre'], params['usuario'], params['clave'], params['correo'])
            db.session.add(user)
            db.session.commit()
            res = results[0]
        except:
            res = results[1]
    
    return json.dumps(res)



@ident.route('/ident/VLogin')
def VLogin():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)



@ident.route('/ident/VPrincipal')
def VPrincipal():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    if "usuario" in session:
        res['nombre']=session['usuario']['nombre']
        res['idUsuario'] = session['usuario']['idUsuario']

    #Action code goes here, res should be a JSON structure

    #Action code ends here
    return json.dumps(res)



@ident.route('/ident/VRegistro')
def VRegistro():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
        
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here

