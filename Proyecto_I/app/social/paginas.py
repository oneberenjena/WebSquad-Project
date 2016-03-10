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
            'msg':['Hubo en error']
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
    print(request.args)
    #GET parameter
    idPagina = request.args['idPagina']
    results = [{'label':'/VPagina', 'msg':[]}, {'label':'/VMiPagina', 'msg':[]}, ]
    res = results[1]
    #Action code goes here, res should be a list with a label and a message
    pagina = Pagina.query.join(Usuario).filter(Usuario.idUsuario==session['usuario']['idUsuario']).first()
    if not pagina and 'usuario' in session:
        res = results[0]
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

    pagina = Pagina.query.join(Usuario).filter(Usuario.idUsuario==idUsuario).first()

    if pagina is None and session['usuario']['idUsuario'] == int(idUsuario):
        res['label'] = '/VPagina/{usuario}'.format(usuario = idUsuario)
    else:
        print('PAgina',pagina)
        res['titulo'] = pagina.titulo
        res['contenido'] = pagina.contenido
    
    if 'usuario' in session:
        res['idUsuario_session'] = session['usuario']['idUsuario']

    #Action code ends here
    return json.dumps(res)

@paginas.route('/paginas/VPagina', methods=['GET'])
def VPagina():
    params = request.get_json()
    idUsuario = request.args['idUsuario']
    res = {
        'titulo': '',
        'contenido': '',
    }
    pagina = Pagina.query.join(Usuario).filter(Usuario.idUsuario==idUsuario).first()
    
    if session['usuario']['idUsuario'] == int(idUsuario):
        if pagina:
            res['titulo'] = pagina.titulo
            res['contenido'] = pagina.contenido

        if "actor" in session:
            res['actor']=session['actor']
        #Action code goes here, res should be a JSON structure

        res['idPagina'] = pagina.idPagina
    else:
        res['label'] = '/VMiPagina/{usuario}'.format(usuario=idUsuario)

    #Action code ends here
    return json.dumps(res)


#Use case code starts here


#Use case code ends here

