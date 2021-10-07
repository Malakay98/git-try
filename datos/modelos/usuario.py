from datos.base_de_datos import BaseDeDatos

#Creo la funcion para obtener todos los usuarios.
#No necesito parametros en esta ocasion, por que no habran valores especificos que se necesiten para la peticion HTTP
def getUsers():
    obtener_usuarios_sql = f"""
       SELECT idUsers, username, email, firstName, lastName, password, id_Rol
       FROM Usuarios
    """
    # Llamo a la clase basededatos y la igualo con una variable
    bd = BaseDeDatos()
    #Devuelvo los valores que se obtuvieron de la peticion HTTP
    return [{'idUsers': registro[0],
             'username': registro[1],
             'email': registro[2],
             'firstName': registro[3],
             'lastName': registro[4],
             'password': registro[5],
             'id_Rol': registro[6]}
              #Por cada registro en la base de datos, quiero aplicar la variable con el metodo asignado
             for registro in bd.ejecutar_sql(obtener_usuarios_sql)]


def getOneUser(id_usuario):
    obtener_un_usuario_sql = f'''
       SELECT idUsers, username, email, firstName, lastName
       FROM Usuarios
       WHERE idUsers = {id_usuario}
    '''
    bd = BaseDeDatos()
    return [{'idUsers': registro[0],
             'username': registro[1],
             'email': registro[2],
             'firstName': registro[3],
             'lastName': registro[4]}
              #Por cada registro en la base de datos, quiero aplicar la variable con el metodo asignado
             for registro in bd.ejecutar_sql(obtener_un_usuario_sql)]

 
def createUsers(username, email, firstName, lastName, password):
    crear_usuario_sql = f"""
        INSERT INTO Usuarios(username, email, firstName, lastName, password)
        VALUES ('{username}', '{email}', '{firstName}', '{lastName}', '{password}')
    """
    bd = BaseDeDatos()
    bd.ejecutar_sql(crear_usuario_sql)
   

def editUser(id_usuario, datos_usuario):
    modificar_usuario_sql = f'''
       UPDATE Usuarios
       SET username='{datos_usuario["username"]}', firstName='{datos_usuario["firstName"]}', lastName='{datos_usuario["lastName"]}', password='{datos_usuario["password"]}'
       WHERE idUsers='{id_usuario}'
    '''
    bd = BaseDeDatos()
    bd.ejecutar_sql(modificar_usuario_sql)


def deleteUser(id_usuario):
    eliminar_usuario_sql = f'''
        DELETE 
        FROM Usuarios 
        WHERE idUsers = '{id_usuario}'
    '''
    bd = BaseDeDatos()
    bd.ejecutar_sql(eliminar_usuario_sql)

# Tambien podria usar "?" en vez de los parametros, esto para incluir mayor seguridad
def login(username, email, password):
    ingresar_datos = f'''
       SELECT idUsers, username, email, password
       FROM Usuarios
       WHERE
       username = '{username}' AND email = '{email}' AND password = '{password}'
    '''
    bd = BaseDeDatos()
    return [{"idUsers": registro[0],
             'username': registro[1],
             "email": registro[2],
             "password": registro[3]
             } for registro in bd.ejecutar_sql(ingresar_datos)]


def createSession(idUser, dt_str):
    crear_sesion_sql = f'''
       INSERT INTO Sesiones(idUser, date_time)
       VALUES('{idUser}','{dt_str}')
    '''
    bd = BaseDeDatos()
    return bd.ejecutar_sql(crear_sesion_sql, True)


def getSession(id_sesion):
    obtener_sesion_sql = f'''
       SELECT idSessions, idUser, date_time FROM Sesiones WHERE idSessions = {id_sesion}
    '''
    bd = BaseDeDatos()
    return [{"idSessions": registro[0],
             "idUser": registro[1],
             "date_time": registro[2]
             } for registro in bd.ejecutar_sql(obtener_sesion_sql)]