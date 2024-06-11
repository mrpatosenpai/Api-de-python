from flask import Flask, jsonify , request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
conexion = MySQL(app)

# Página principal
@app.route('/')
def index():
    return '¡Hola! Esta es la página principal.'

@app.route('/listatareas', methods=['GET'])
def listatareas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tareas"
        cursor.execute(sql)
        datos = cursor.fetchall()
        tareas =[]
        for fila in datos:
            tarea = {
                'id_tarea': fila[0],
                'nombre': fila[1],
                'fechainicio': str(fila[2]),
                'fechafinal': str(fila[3]),
                'estado': fila[4]
            }
            tareas.append(tarea)
        return jsonify(tareas)

    except Exception as ex:
        return jsonify({'error': 'Error al obtener las tareas', 'mensaje': str(ex), 'exito': False})

@app.route('/listausuarios', methods=['GET'])
def listausuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios =[]
        for fila in datos:
            usuario = {
                'id_user': fila[0],
                'nombre_user': fila[1],
                'apellido_user': fila[2],
                'email_user': fila[3],
                'usuario_user': fila[4],
                'rol_user':fila[6]
            }
            usuarios.append(usuario)
        return jsonify(usuarios)

    except Exception as ex:
        return jsonify({'error': 'Error al obtener los usuarios', 'mensaje': str(ex), 'exito': False})
    

@app.route('/buscartareas', methods=['GET'])
def buscartareas():
    consulta = 'SELECT * FROM tareas'
    filtro = []
    parametros = []

    nombre = request.args.get('nombre')
    if nombre:
        filtro.append("nombre LIKE %s")
        parametros.append(f"%{nombre}%")
    if not filtro:
        return jsonify({'message' :'no tiene parametros la busqueda'}),400
    
    fechainicio = request.args.get('fechainicio')
    if fechainicio:
        filtro.append("fechainicio LIKE %s")
        parametros.append(f"%{fechainicio}%")
    if not filtro:
        return jsonify({'message' :'no tiene parametros la busqueda'}),400

    fechafinal = request.args.get('fechafinal')
    if fechafinal:
        filtro.append("fechafinal LIKE %s")
        parametros.append(f"%{fechafinal}%")
    if not filtro:
        return jsonify({'message' :'no tiene parametros la busqueda'}),400
    
    estado = request.args.get('estado')
    if estado:
        filtro.append("estado LIKE %s")
        parametros.append(f"%{estado}%")
    if not filtro:
        return jsonify({'message' :'no tiene parametros la busqueda'}),400

    consulta += " WHERE " + " AND ".join(filtro)
    cursor = conexion.connection.cursor()
    cursor.execute(consulta, parametros)
    datos = cursor.fetchall()
    tareas =[]
    for fila in datos:
        tarea = {
        'id_tarea': fila[0],
        'nombre': fila[1],
        'fechainicio': str(fila[2]),
        'fechafinal': str(fila[3]),
        'estado': fila[4]
        }
        tareas.append(tarea)
    return jsonify(tareas)
@app.route('/creartarea',methods = ['POST'])
def creartarea():
    tarea = request.json
    nombret = tarea['nombre']
    fechain = tarea['fechainicio']
    fechafin = tarea['fechafinal']
    estado = tarea['estado']
    cursor = conexion.connection.cursor()
    cursor.execute("INSERT INTO tareas(nombre, fechainicio, fechafinal, estado)VALUES(%s,%s,%s,%s)",(nombret,fechain,fechafin,estado))
    conexion.connection.commit()
    return jsonify({'message': 'tarea agregada con exito'}),201

@app.route('/actualizart/<int:id_tarea>', methods=['PUT'])
def actualizart(id_tarea):
    actu = request.json
    nombre = actu['nombre']
    fechain = actu['fechainicio']
    fechafin = actu['fechafinal']
    estado = actu['estado']
    cursor = conexion.connection.cursor()
    cursor.execute("UPDATE tareas SET nombre = %s, fechainicio = %s, fechafinal = %s, estado = %s WHERE id_tarea = %s", (nombre, fechain, fechafin, estado, id_tarea))
    conexion.connection.commit()
    return jsonify({'message': 'tarea actualizada con éxito'}), 200

app.route('/eliminart/<id_tarea>', methods=['DELETE'])
def eliminart(codigo):
    cursor = conexion.connection.cursor()
    cursor.execute("DELETE FROM tareas WHERE id_tarea = %s",[codigo])
    conexion.connection.commit()

    return jsonify({'message':'Tarea eliminada'})

if __name__ == '__main__':
    app.config.from_object(config['config'])
    app.run(debug=True)
