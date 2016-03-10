from flask import request, session, Blueprint, json

paginas = Blueprint('paginas', __name__)

from base import db, Usuario, Pagina

@paginas.route('/paginas/AModificarPagina', methods=['POST'])
def AModificarPagina():
    print (session)
    #POST/PUT parameters
    params = request.get_json()
    results = [
        {
            'label':'/VPagina',
            'msg':['Cambios almacenados']
        },
        {
            'label':'/paginas/AModificarPagina',
            'msg':['El título debe tener más de 5 caracteres']
        }
    ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    if 'usuario' in session and 'titulo' in params and len(params['titulo']) >= 5:
        pagina = Pagina.query.join(Usuario).filter(Usuario.idUsuario==session['usuario']['idUsuario']).first()
        if pagina:
            pagina.titulo = params['titulo']
            pagina.contenido = params['contenido']
        else:
            pagina = Pagina(titulo=params['titulo'], contenido=params['contenido'], usuario_id=session['usuario']['idUsuario'])
            db.session.add(pagina)
        db.session.commit()
        res = results[0]
        res['label'] += '/{}'.format(session['usuario']['idUsuario'])
    else:
        res = results[1]

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)

@paginas.route('/paginas/APagina')
def APagina():
    #GET parameter
    idPagina = request.args['idPagina']
    results = [{'label':'/VPagina', 'msg':[]}, {'label':'/VMiPagina', 'msg':[]}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    #Cuando la página exista, ir directamente a ella. 
    #Si no exite ir al editor de páginas.
    res['label'] = res['label'] + '/' + repr(1)

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@paginas.route('/paginas/VMiPagina')
def VMiPagina():
    #GET parameter
    idUsuario = request.args['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['titulo'] = "El título de mi página"
    res['contenido'] = "<h3>¿No es bella mi página?</h3><p>Claro que <b>si</b>.</p>"
    

    #Action code ends here
    return json.dumps(res)

@paginas.route('/paginas/VPagina', methods=['GET'])
def VPagina():
    params = request.get_json()
    idUsuario = request.args['idUsuario']
    res = {
        'titulo': '',
        'contenido': ''
    }
    pagina = Pagina.query.join(Usuario).filter(Usuario.idUsuario==session['usuario']['idUsuario']).first()
    print(pagina.__dict__)
    if pagina:
        res['titulo'] = pagina.titulo
        res['contenido'] = pagina.contenido
    
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)

@paginas.route('/paginas/VPagina', methods=['GET'])
def VPaginaDetalle():
    params = request.get_json()
    idUsuario = request.args['idUsuario']
    results = [
        {
            'msg': ['Debes crear una pagina'],
            'label': '/VPagina'
        },
        {
            'label': '/VPaginaDetalle'
        }
    ]
    res['label'] += '/{}'.format(session['usuario']['idUsuario'])
    pagina = Pagina.query.join(Usuario).filter(Usuario.idUsuario==session['usuario']['idUsuario']).first()
    
    if pagina:
        res['titulo'] = pagina.titulo
        res['contenido'] = pagina.contenido
        
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)



#Use case code starts here


#Use case code ends here

