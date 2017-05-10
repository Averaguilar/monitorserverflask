# 06 Mayo 2017, maqueta del engine central de monitoreo movimientos de placas.
# Versión 0.1.0.0

from flask import Flask
import pyodbc

app = Flask(__name__)

@app.errorhandler(404) # función para atrapar el error 400 pagina no encontrada
def noloenconte(error):
    return "no existe esa pag."

@app.route(r'/') # Esto define un URL desde el cual la fincion ini() de abajo definira que se regresa en ese URL
def init():
    return "I am alive: Monitoreo Engine"

@app.route(r'/post/')
@app.route(r'/post/<placa>/<horaDeRegistro>/<movimiento>/<punto>')
# def tunombre(nombre='slenderman', edad='300'):
def regMovimiento(placa='RB64322', horaDeRegistro='2017-05-09 2020:06:33.144165', movimiento='S', punto=1):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=AUGUSTO-LENOVO\SQLEXPRESS;DATABASE=MONITORPLACAS')
    cursor = cnxn.cursor()
    SQLcommand = format("SELECT DISTINCT id, MUNICIPIO, NOMBRE, APELLIDO_P FROM PADRON_PLACAS_NL WHERE PLACAS = '{}'".format(placa))
    cursor.execute(SQLcommand)
    tables = cursor.fetchall()
    print(placa)
    print(tables)
    idPlaca = tables[0][0]
    print(idPlaca)
    municipio = tables[0][1]
    print(municipio)
    nombre = tables[0][2]
    print(nombre)
    apellido = tables[0][3]
    print(apellido)

    cursor.execute("INSERT INTO BITACORA_MOVIMIENTOS(ID_PLACA, TIPO_MOVIMIENTO, PUNTO_LECTURA, HORA_LECTURA, FECHA_LECTURA) values (?, ?, ?, ?, ?)", idPlaca, movimiento, punto, horaDeRegistro, horaDeRegistro)
    cnxn.commit()
    # print("consulta > " + SQLcommand)
    # print("resultado > ", tables)
    return horaDeRegistro + ", placa " + placa + ", municipio " + municipio + ", movimiento " + movimiento + ", punto de acceso " + str(punto) + ", nombre " + nombre + " " + apellido

# @app.before_request # ejecuta funcion antes de la peticion del URL, por ejemplo logear antes de conectar a BD.
# def antes_peticion():
#     if 'username' not in session and request.endpoint in ['home','busqueda','titulo']:
#         return redirect(url_for('login'))

# @app.after_request # ejecuta funcion despues de la peticion de URL, por ejemplo cerrar conexion BD
# def despues_peticion(peticion):
#     return peticion

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug = True)
