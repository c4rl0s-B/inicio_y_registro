from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0_9.+_-]+@^[a-zA-Z0_9._-]+,[a-zA-Z]+$')

class Usuario:

    def __init__(self,data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s,%(apellido)s,%(email)s,%(password)s,NOW(),NOW())"
        return connectToMySQL('inicio_registro_sesion').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios"
        usuarios_en_db = connectToMySQL('cinepedia').query_db(query)
        #lista vacia de usuarios se llena con clase usuarios
        usuarios = []
        #por cada usuario que encuentre en usuarios_en_db
        for usuario in usuarios_en_db:
            #voy a crear una instancia de la clase Usuario al final de la lista usuarios

            usuarios.append(cls(usuario))

        return usuarios
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email=%(email)s"
        usuario_en_db = connectToMySQL('inicio_registro_sesion').query_db(query,data)

        print("USUARIO EN DB",usuario_en_db)
        if not usuario_en_db:
            return None
        return cls(usuario_en_db[0])


    @staticmethod
    def validar_registro(formulario):
        es_valido = True

        if len(formulario['nombre']) < 2:
            flash("El nombre deve tener al menos 2 caracteristicas","registro")
            es_valido = False

        if len(formulario['apellido']) < 2:
            flash("El apellido deve tener al menos dos caracteres", "reguistro")
            es_valido = False

        if not EMAIL_REGEX.match(formulario['email']):
            flash("El emailno tiene un formato válido", "registro")
            es_valido = False
        elif Usuario.get_by_email({'email':formulario['email']}):
            print(Usuario.get_by_email({'email':formulario['email']}))
            flash("Ya existe una cuenta con este email",'registro')
            es_valido = False

        if len(formulario['password'])<8:
            flash("La contraseña deve tener al menos 8 caracteristicas")
            es_valido = False

        if formulario['password'] != formulario['password_conf']:
            flash("Las contraseñas no coinciden", "registro")
            es_valido = False

        return es_valido
        