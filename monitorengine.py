# 06 Mayo 2017, maqueta del engine central de monitoreo movimientos de placas.
# Versión 0.1

from flask import Flask
import pyodbc

app = Flask(__name__)

@app.errorhandler(404) 
def noloenconte(error):
    return "no existe esa pag."

@app.route(r'/') 
def init():
    return "I am alive: Monitoreo Engine"

@app.route(r'/enviaplaca') 
def tienesque():
    return "tienes que enviar una placa!!"

@app.route(r'/enviaplaca/<placa>')
def echoplaca():
    return "Numero de placa: {}".format(placa)

# @app.route(r'/enviaplaca/<placa>/<horaDeRegistro>')
# @app.route(r'/enviaplaca/<placa>/<horaDeRegistro>/<movimiento>')
@app.route(r'/enviaplaca/<placa>/<horaDeRegistro>/<movimiento>/<int:punto>', methods=["GET"])
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

    return horaDeRegistro + ", placa " + placa + ", municipio " + municipio + ", movimiento " + movimiento + ", punto de acceso " + str(punto) + ", nombre " + nombre + " " + apellido

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug = True)
