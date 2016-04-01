from collections import OrderedDict
from flask import request, session, Blueprint, json
from base import *
import sqlalchemy

foro = Blueprint('foro', __name__)

def parsearPublicaciones(hilo):
    publicaciones_db = Publicacion.query.join(
        Usuario, Publicacion.autor_id == Usuario.idUsuario
    ).add_columns(
        Usuario.nombre
    ).filter(Publicacion.hilo_id == hilo.idHilo).all()
    
    publicacion = publicaciones_db[0][0]
    autor = publicaciones_db[0][1]
    pubRaiz = {
        'idPublicacion': publicacion.idPublicacion,
        'titulo': publicacion.titulo,
        'contenido': publicacion.contenido,
        'fecha': publicacion.fecha.isoformat(),
        'padre_id': publicacion.padre_id,
        'autor_id': publicacion.autor_id,
        'autor': autor,
        'respuestas': []
    }
    publicaciones = pubRaiz
    publicaciones_raw = {pubRaiz['idPublicacion']: pubRaiz}
    # Toda publicación hija está hecha despúes que su padre, luego, si ordenamos por fecha
    # las publicaciones padre siempre van a estar agregadas antes que las hijas
    i = 0
    for p in publicaciones_db:
        if i == 0:
            i += 1
            continue
        print(p)
        publicacion = p[0]
        autor = p[1]
        
        publicacion = {
            'idPublicacion': publicacion.idPublicacion,
            'titulo': publicacion.titulo,
            'contenido': publicacion.contenido,
            'fecha': publicacion.fecha.isoformat(),
            'padre_id': publicacion.padre_id,
            'autor_id': publicacion.autor_id,
            'autor': autor,
            'respuestas': []
        }
        if publicacion['padre_id'] is None:
            publicaciones[publicacion['idPublicacion']] = publicacion
            publicacion['respuestas'] = []
        else:
            if 'respuestas' in publicaciones_raw[publicacion['padre_id']]:
                publicaciones_raw[publicacion['padre_id']]['respuestas'] += [publicacion]
            else:
                print(publicaciones_raw, )
                publicacions_raw[publicacion['padre_id']]['respuestas'] = [publicacion]

        publicaciones_raw[publicacion['idPublicacion']] = publicacion
        
    return publicaciones



@foro.route('/foro/AComentar', methods=['POST'])
def AComentar():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/p', 'msg':['Comentario realizado']}, {'label':'/VPublicacion/pagina', 'msg':['Error al realizar comentario']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    #En caso de error
    res['label'] = res['label'] + '/' + str(params['url'])

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)


@foro.route('/foro/AObtenerComentarios')
def AObtenerComentarios():
    #GET parameter
    url = request.args['url']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    hilos = Hilo.query.filter_by(pag_id=url).all()
    res['comentarios'] = [parsearPublicaciones(hilo) for hilo in hilos]
    #Action code ends here
    return json.dumps(res)
    
@foro.route('/foro/AElimForo', methods=['POST'])
def AElimForo():
    #GET parameter
    idForo = request.get_json()['idForo']
    results = [{'label':'/VForos', 'msg':['Foro eliminado']}, {'label':'/VForo', 'msg':['No se pudo eliminar el foro']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    
    if idForo:
        foro = Foro.query.filter_by(idForo=idForo).first()
        if foro and int(foro.autor_id) == int(session['usuario']['idUsuario']):
            db.session.delete(foro)
            db.session.commit()
        else:
            res = results[1]
    else:
        res = results[1]

    res['label'] = res['label'] + '/' + str(session['usuario']['idUsuario'])

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@foro.route('/foro/APublicar', methods=['POST'])
def APublicar():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VForo', 'msg':['Publicación realizada']}, {'label':'/VPublicacion', 'msg':['Error al realizar publicación']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    if 'usuario' in session:
        publicacion = Publicacion(
            titulo = params['titulo'],
            contenido = params['contenido'], 
            autor_id = session['usuario']['idUsuario'],
            tipo = params['tipo'],
            foro_id = params['foro_id'] if params['tipo'] == 'foro' else None,
            pag_id = params['pag_id'] if params['tipo'] == 'pagina' else None,
            padre_id = params['padre_id']
        )
        db.session.add(publicacion)
        db.session.commit()
        
        if params['padre_id'] is None:
            if params['tipo'] == 'foro':
                hilo = Hilo(titulo=params['titulo'], pubRaiz=publicacion, tipo=1, foro_id = params['foro_id'], pag_id=None)
            elif params['tipo'] == 'pagina':
                hilo = Hilo(titulo=params['titulo'], pubRaiz=publicacion, tipo=0, foro_id = None, pag_id=params['pag_id'])
            db.session.add(hilo)
            db.session.commit()
            publicacion.hilo_id = hilo.idHilo
        else:
            pubPadre = Publicacion.query.filter_by(idPublicacion=publicacion.padre_id).first()
            publicacion.hilo_id = pubPadre.hilo_id
        
        db.session.add(publicacion)
        db.session.commit()
        
    else:
        res = results[1]
        
    
        
    res['label'] = (res['label'] + '/' + str(params['foro_id']) if params['tipo'] == 'foro' else "/p/" + params['pag_id'])

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@foro.route('/foro/AgregForo', methods=['POST'])
def AgregForo():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VForos', 'msg':['Foro creado']}, {'label':'/VForos', 'msg':['No se pudo crear el foro']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    if (params['titulo']):
        try:
            foro = Foro(params['titulo'],session['usuario']['idUsuario'])
            db.session.add(foro)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            print("Hice rollback")
            res = results[1]
            
    else:
        res = results[1]
    

    res['label'] = res['label'] + '/' + str(session['usuario']['idUsuario'])

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@foro.route('/foro/VComentariosPagina')
def VComentariosPagina():
    #GET parameter
    idPaginaSitio = request.args['idPaginaSitio']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idPagina'] = 1

    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VForo')
def VForo():
    #GET parameter
    idForo = request.args['idForo']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idForo'] = idForo
    res['idUsuario'] = session['usuario']['idUsuario']
    
    # ASCANDER LO PUSO
    #res['idMensaje'] = 0 #Nueva publicación
    
    hilos = Hilo.query.filter(Hilo.foro_id==idForo).all()
    
    
    res['hilos'] = [parsearPublicaciones(hilo) for hilo in hilos]

    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VForos')
def VForos():
    #GET parameter
    idUsuario = request.args['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['data0'] = [
        {
          'idForo': foro.idForo, 
          'nombre': foro.titulo,
          'esAutor': int(foro.autor_id) == int(session['usuario']['idUsuario'])
        } for foro in Foro.query.all()
    ]

    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VPublicacion')
def VPublicacion():
    #GET parameter
    #idMensaje = request.args['idMensaje']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    #res['idForo'] = 1

    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here

