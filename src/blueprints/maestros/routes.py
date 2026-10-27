from flask import Blueprint, jsonify, request
from database import mysql
 
maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix = '/api/maestros'
)
 
def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))
 
 
@maestros_bp.route('/maestros', methods=['GET'])
def lista_maestros():
    cursor = None
 
 
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
        SELECT idmestro, nombre, apaterno, amaterno, correo
        FROM maestros """)
 
        datos = cursor.fetchall()
        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]
 
        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200
 
 
    except Exception:
        return jsonify({
            'mensaje': 'Error al consultar los maestros',
            'exito': False
        }), 500
 
 
    finally:
        if cursor is not None:
            cursor.close()

def leer_maestro_bd(idmaestro):
    try:
        cursor=mysql.connection.cursor()
        sql="select * from maestros where idmaestro={0}".format(idmaestro)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            maestro={
                "idmaestro":datos[0], "nombre":datos[1],
                "apaterno":datos[2], "amaterno":datos[3],
                "correo":datos[4]
            }
            return maestro
        else:
            return None
 
    except Exception as ex:
        raise ex
 
@maestros_bp.route("/<mat>", methods=["GET"])
def leer_maestro(mat):
    try:
        maestro=leer_maestro_bd(mat)
        if maestro != None:
            return jsonify({'maestro':maestro,'mensaje':"Maestro encontrado", 'exito':True})
        else:
            return jsonify({'maestro':maestro, 'mensaje':'Maestro no encontrado', 'exito':False})
    except Exception as ex:
        return jsonify({"message":"error {}".format(ex), 'exito':False})
 
 
@maestros_bp.route("/", methods=['POST'])
def registrar_maestro():
    try:
        maestro=leer_maestro_bd(request.json['idmaestro'])
        if maestro != None:
            return jsonify({'mensaje':'Maestro ya existe, no se permiten duplicados', 'exito':False})
        else:
            cursor=mysql.connection.cursor()
            sql="""insert into maestros (idmaestro,nombre,apaterno,amaterno,correo) values('{0}','{1}','{2}','{3}','{4}')""".format(request.json['idmaestro'],request.json['nombre'],request.json['apaterno'],request.json['amaterno'],request.json['correo'] )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje':"Maestro registrado", 'exito':True})
           
    except Exception as ex:
        return jsonify({'mensaje': "error {}".format(ex), 'exito': False})
 
 
@maestros_bp.route('/<mat>', methods=['PUT'])
def actualizar_curso(mat):
    try:
        maestro = leer_maestro_bd(mat)
        if maestro != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE maestros SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}' WHERE idmaestro = {4}""".format(request.json['nombre'],request.json['apaterno'], request.json['amaterno'], request.json['correo'], mat)
            cursor.execute(sql)
            mysql.connection.commit()  
            return jsonify({'mensaje': "Maestro actualizado.",'exito': True})
        else:
            return jsonify({'mensaje': "Maestro no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "error {0}".format(ex), 'exito': False})
 
 
@maestros_bp.route('/<mat>', methods=['DELETE'])
def eliminar_maestro(mat):
    try:
        maestro=leer_maestro_bd(mat)
        if maestro != None:
            cursor=mysql.connection.cursor()
            sql="DELETE FROM maestros WHERE idmaestro = {0}".format(mat)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje':"Maestro eliminado", 'exito':True})
        else:
            return jsonify({'mensaje':"Maestro no eliminado", 'exito':False})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito':False})
 
def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404
 
 
if __name__ == "__main__":
 
    app.config.from_object(config["development"])
 
    app.register_error_handler(404, pagina_no_encontrada)
 
    app.run(host="0.0.0.0", port=5000)