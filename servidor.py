from enum import auto
import re
from sqlite3.dbapi2 import register_adapter
from flask import Flask, request, jsonify
from datos.modelos.usuario import getSession
from servicios.autenticacion import autenticacion
from datos.modelos import noticias


app = Flask(__name__)

# Obtener los datos de todos los usuarios.
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(autenticacion.getUsers())


#Obtener los datos de un usuario mediante su ID "idUsers"
@app.route('/usuarios/<id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    try:
        usuario = autenticacion.GetUserById(id_usuario)
        return jsonify(usuario)
    except Exception:
        return 'Usuario no encontrado', 404


# Crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos_usuario = request.get_json()
    if 'username' not in datos_usuario:
        return 'El nombre de usuario es requerido', 412 #Error "412"; El servidor no es capaz de cumplir con algunas de las condiciones impuestas por el "navegador" en nuestra petición​
    if 'email' not in datos_usuario:
        return 'El email es requerido', 412
    if 'firstName' not in datos_usuario:
        return 'El nombre es requerido', 412
    if 'lastName' not in datos_usuario:
        return 'El apellido es requerido', 412
    if 'password' not in datos_usuario:
        return 'La clave es requerida', 412

    autenticacion.createUsers(datos_usuario['username'], datos_usuario['email'], datos_usuario['firstName'], datos_usuario['lastName'], datos_usuario['password'])
    return jsonify(f'Usuario creado exitosamente. Usuario: ', datos_usuario), 200 #Codigo de estado "200": informa que todo se ha procesado de manera correcta.


#Modificar los valores de un usuario
@app.route('/usuarios/<id_usuario>', methods=['PUT'])
def modificar_usuario(id_usuario):
    datos_usuario = request.get_json()
    if 'username' not in datos_usuario or datos_usuario['username'] == '':
        return "El nombre de usuario es requerido", 412
    if 'firstName' not in datos_usuario or datos_usuario['firstName'] == '':
        return "El nombre es requerido", 412
    if 'lastName' not in datos_usuario or datos_usuario['lastName'] == '':
        return "El apellido es requerido", 412
    if 'password' not in datos_usuario or datos_usuario['password'] == '':
        return "La clave es requerida", 412

    autenticacion.editUsers(id_usuario, datos_usuario)
    return 'Usuario modificado', 200    


# Elimina al usuario a partir del ID del mismo
@app.route('/usuarios/<id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    autenticacion.deleteUser(id_usuario)
    return jsonify(f'Usuario eliminado. ID del usuario: ', id_usuario), 200


# Iniciamos sesion con un usuario existente
@app.route('/login', methods=['POST'])
def login():
    datos_usuario = request.get_json()
    if 'username' not in datos_usuario:
        return 'El nombre de usuario es requerido', 412
    if 'email' not in datos_usuario:
        return 'El email es requerido', 412
    if 'password' not in datos_usuario:
        return 'La clave es requerida', 412
    
    id_sesion = autenticacion.login(datos_usuario['username'], datos_usuario['email'], datos_usuario['password'])
    if id_sesion:
        return f"Usuario logueado exitosamente: idSession {id_sesion}", 200
    else:
        return f"Usuario, correo o clave equivocada, intentelo de nuevo", 200


# Obtenemos la sesion del usuario
@app.route('/login/sesion/<id_sesion>', methods=['GET'])
def obtener_sesion(id_sesion):
    return autenticacion.validateSession(id_sesion)

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)
