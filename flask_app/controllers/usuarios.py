from flask_app import app
from flask import render_template,request,redirect, flash, session
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt #Importamos Bcrypt

bcrypt = Bcrypt(app) #Generamos un objeto llamado bcrypt


@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registrar_usuario', methods=["POST"])
def crear_usuario():
    if not Usuario.validar_registro(request.form):
        print("Usuario Invalido")
        return redirect('/')

    pass_hasheado = bcrypt.generate_password_hash(request.form['password'])

    datos_usuario_registro= {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email':request.form['email'],
        'password': pass_hasheado
    }
    nuevo_id= Usuario.save(datos_usuario_registro)
    session['usuario.id']=nuevo_id
    return redirect('/pag_inicial')