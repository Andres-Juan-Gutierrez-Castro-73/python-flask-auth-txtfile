from flask import Flask, render_template, request
import re

#RUTAS DE FLASK
app = Flask(__name__)

#RETORNO DE LA VISTA RAIZ
@app.route('/')
def registroPagina():
    return  render_template('/login.html')

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    error = None
    if request.method == 'POST' and validar_informacion(
            request.form['usuario'],
            request.form['nombre'],
            request.form['apellido'],
            request.form['clave'],
            request.form['email'],
            request.form['telefono'],
        ):
        return render_template("/index.html")
    else:
        return  render_template('/login.html')
 
@app.route('/inicio', methods=['POST', 'GET'])
def inicio():
    if request.method == 'POST' and buscar(request.form['name'], request.form['pass']):
        return render_template('/index.html')
    else:
        return render_template('/login.html')

#LOGICA PARA LA APLICACION DE PRODUCTOS

#PROBLEMA1
""" Estos datos deben quedar guardados en el archivo datos.txt, cada campo debe quedar
separado por comas, ejemplo:
    pedro,clavepedro1, Pedro, Perez, pedro@hotmail.com,39949494
    juan,clavejuan,Juan22, Gomez,juan@gmail.com,38847474 """

#DEFINIMOS UNA FUNCION QUE GUARDE LA INFORMACION Y EN ARCHIVO Y QUE VAYA LLENANDO TODOS LOS REGISTROS
def guardar_informacion(usuario, nombre, apellido, contrasena, correo_electronico, telefono):
    #CREAMOS UNA VARIABLE QUE CONCATENE LA INFORMACION ANTERIOR (FORMATO CON EL QUE VA ESTAR EN EL ARCHIVO .TXT)
    concatenacion_datos = usuario + ", " + nombre + ", " + apellido + ", " + contrasena + ", " + correo_electronico + ", " + telefono
    with open('datos.txt', 'a') as archivo:
        lineas = [
            concatenacion_datos,
            "\n",
        ]
        archivo.writelines(lineas)

#IMPLEMENTAMOS LA FUNCION
#guardar_informacion(usuario, nombre, apellido, contrasena, correo_electronico, telefono)

#PROBLEMA 2
""" Debe validar los campos así:
- Ningún campo puede quedar vacío
- El campo email debe contener mínimo una "@" y un punto
- El campo teléfono debe ser numérico
- La clave debe tener una longitud de mínimo 8 caracteres y debe contener minimo
un número """
def validar_informacion(usuario, nombre, apellido, contrasena, correo_electronico, telefono):
    if (len(usuario) == 0 or
        len(nombre) == 0 or
        len(apellido) == 0 or
        len(contrasena) == 0 or
        len(correo_electronico) == 0 or
        len(telefono) == 0
    ):
        print("Por favor rellene todos lo campos")
    else:
        #VALIDAMOS QUE LA CONTRASEÑA CONTENGA 8 O MAS CARACTERES
        if (len(contrasena) >= 8):
            print("La contraseña tiene la longitud requerida")
            #CON LA LIBRERIA RE VALIDAMAMOS QUE LA CONSTRASEÑA CONTENCA LETRAS, NUMEROS Y CARACTERES ESPECIALES
            if re.search("[a-zA-Z]", contrasena) and re.search("[0-9]", contrasena) and re.search("[^a-zA-Z0-9]", contrasena):
                #print("La cadena contiene letras, números y caracteres especiales")
                guardar_informacion(usuario, nombre, apellido, contrasena, correo_electronico, telefono)
                #RETORNAMOS UN TRUE
                return True
            else:
                print("La cadena no contiene letras, números y/o caracteres especiales")
                return False
        else:
            print("La contraseña NO tiene la longitud requerida")
            return False
#IMPLEMENTAMOS LA FUNCION
#validar_informacion(usuario, nombre, apellido, contrasena, correo_electronico, telefono)

#PROBLEMA 3
"""CREAMOS UNA FUNCION QUE LEA UNA ARCHIVO TXT
ESE DEBE LEER DOS INPUTS Y RETORNAR UNA TRUE EN CASO DE
QUE ENCUENTRE LA PALABRA"""

#CREAMOS UNA FUNCION LA CUAL NOS PERMITA BUSCAR UNA PALABRA DENTRO DEL ARCHIVO DE TEXTO
def buscar(palabra1, palabra2):
    # ABRIMOS EL ARCHIVO EN MODO DE LECTURA
    with open("datos.txt", "r") as archivo:
        # EL CONTENIDO LO GUARDAMOS EN UNA VARIABLE
        contenido = archivo.read()

        # CPMPROBAMOS QUE EL INPUT SE ENCUENTRA EN LA VARIABLE
        if palabra1 in contenido and palabra2 in contenido and palabra1 !="" and palabra2 !="":
            return True
        else:
            return False
    # CERRAMOS EL ARCHIVO
    archivo.close()

#CONFIGURACION DEL LOCALHOST Y DEL DEBUG
if __name__ == '__main__':  
    app.run('127.0.0.1', 5000, debug=True)