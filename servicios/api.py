from flask import Flask, jsonify, abort, make_response, request, jsonify
from servicios.configurador import *


app_api = Flask(__name__)
config = Configurador

""" Errores """
@app_api.errorhandler(404)
def not_fount(error):
    return make_response(jsonify({'error': 'No Encontrado'}), 404)

@app_api.errorhandler(500)
def not_fount(error):
    return make_response(jsonify({'error': error}), 500)

""" Apis """
@app_api.route("/proyectos/", methods=["GET"])
def get_proyectos():
    """
    buscar los proyectos desde el gestor de proyectos
    :return:
    """
    lista_proyectos = []
    for proyecto in config.gestor_proyecto.obtener_todos_los_proyectos():
        p = {}
        p['nombre_proyecto'] = str(proyecto.nombre)
        p['tipo_proyecto'] = str(proyecto.tipo_proyecto)
        p['descripcion'] = str(proyecto.descripcion)
        lista_proyectos.append(p)

    return jsonify(lista_proyectos)


@app_api.route("/proyecto/<string:id>/", methods=["GET"])
def get_proyecto(id):
    """
    Recupera un proyecto o
    :param id:
    :return:
    """
    try:
        proyecto = config.gestor_proyecto.recuperar_proyecto(id)
        p = {}
        p['nombre_proyecto'] = str(proyecto.nombre)
        p['tipo_proyecto'] = str(proyecto.tipo_proyecto)
        p['descripcion'] = str(proyecto.descripcion)

        lista_componentes = []
        for componente in config.gestor_componente.obtener_componentes_del_proyecto(id):
            c={}
            c['nombre'] = str(componente.nombre)
            c['tipo_componente'] = str(componente.tipo_componente)
            c['identificacion'] = str(componente.identificacion)
            lista_componentes.append(c)

        p['lista_componentes'] = lista_componentes
    except:
        return make_response(jsonify({'error': "Al recuperar el id:" + id}), 500)
    return jsonify(p)


@app_api.route("/proyecto/", methods=["POST"])
def post_proyecto():
    """
    Recupera un proyecto o
    :param id:
    :return:
    """
    datos = request.get_json()
    nombre_proyecto = datos['nombre_proyecto']
    tipo_proyecto = datos['tipo_proyecto']
    descripcion = datos['descripcion']
    fecha_fin = datos['fecha_fin']
    config.gestor_proyecto.crear_proyecto(nombre_proyecto, tipo_proyecto, descripcion, fecha_fin)
    config.gestor_proyecto.guardar_proyecto()
    return "Proyecto Guardado", 201