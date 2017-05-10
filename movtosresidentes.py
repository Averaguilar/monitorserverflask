# Augusto Vera y Aguilar, 22 de Abril 2017
# primer ensayo de script python que llama a un servidor de web flask el servidor se llama Flaktest.py
# Puse el servidor prototipo de Flask (Flasktest.py) en la virtual de windows 7 virtualbox "python3.6 con flask"

import urllib.request
import time
import random
import pyodbc
import datetime

# cuantas placas para la simulación y el intervalo inf y superior de delta en segundos de salidas y entradas.
placasEnMuestra, rangoInfSegS, rangiSupSegS, rangoInfSegE, rangiSupSegE = 100, 5, 20, 20, 40
municipio = "'SAN PEDRO'"
datetime.time.
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=AUGUSTO-LENOVO\SQLEXPRESS;DATABASE=MONITORPLACAS')
cursor = cnxn.cursor()
# ejecuto el cursor que saca la muestra de placas para la simulación.
cursor.execute("SELECT DISTINCT TOP "+ str(placasEnMuestra) + " PLACAS FROM PADRON_PLACAS_NL WHERE MUNICIPIO = " + municipio)
muestraPlacasSP =  cursor.fetchall()


print('long de muestra de placas: ', placasEnMuestra)

# saco los tiempos de salida y entrada con deltas
tiemposSalida, tiemposLlegada = [], []
ahoraMismo = datetime.datetime.now()
for i in range(placasEnMuestra):
    tiemposSalida.append(ahoraMismo + datetime.timedelta(seconds=random.randint(rangoInfSegS,rangiSupSegS)))
    tiemposLlegada.append(tiemposSalida[i] + datetime.timedelta(seconds=random.randint(rangoInfSegE,rangiSupSegE)))

# armo la tabla completa de placas, tiempo entrada, tiempo salida, movimiento, y punto del movto
tablaPlacasTiempos = [] # inicializo la tabla que contendra todos los datos para la simulacion
# Estructura de cada linea la tablaPlacasTiempos:

for i in range(placasEnMuestra):
    tablaPlacasTiempos.append([muestraPlacasSP[i][0], tiemposSalida[i], tiemposLlegada[i], 'N', random.randint(1,4), random.randint(1,4)])
    # estructura de cada linea de tablaPlacasTiempos:
    # | [0] placa | [1] tiemposalida | [2] tiempoentrada | [3] movimiento(N,S,E) | [4] puntosalida | [5] puntoentrada |
    # checar la tabla de CATALOGO_ACCESOS en la BD MONITORPLACAS en SQLServer
print(tablaPlacasTiempos)

idx = 0
try:
    while True:
        idx += 1
        if idx > placasEnMuestra:
            idx = 0

        ahoraMismo = datetime.datetime.now() # ahoraMismo es el puntero que sirve para ver si ya se vencieron los tiempos de salida y entrada en cada barrida
        if tablaPlacasTiempos[idx][3] == 'N' and tablaPlacasTiempos[idx][1] <= ahoraMismo: # si no se ha movido (N) y ahoramismo ya rebasó el momento de salida
            tablaPlacasTiempos[idx][3] = 'S'
            # envía al monitor de movimientos de residentes: placa, hora del registro, movimiento 'S', por donde salió
            with urllib.request.urlopen('http://127.0.0.1:5000/post/{}/{}/{}/{}'.format(tablaPlacasTiempos[idx][0], ahoraMismo, tablaPlacasTiempos[idx][3], tablaPlacasTiempos[idx][4])) as f:
                print(f.read(300).decode('utf-8'))
        elif tablaPlacasTiempos[idx][3] == 'S' and tablaPlacasTiempos[i][2] <= ahoraMismo: # si ya salio (S) y ahoramismo ya rebasó el momento de entrada
            tablaPlacasTiempos[idx][3] = 'E'
            # envía al monitor de movimientos de residentes: placa, hora del registro, movimiento 'E', por donde entró
            with urllib.request.urlopen('http://127.0.0.1:5000/post/{}/{}/{}/{}'.format(tablaPlacasTiempos[idx][0], ahoraMismo, tablaPlacasTiempos[idx][3], tablaPlacasTiempos[idx][5])) as f:
                print(f.read(300).decode('utf-8'))
        elif tablaPlacasTiempos[idx][3] == 'E' and tablaPlacasTiempos[idx][2] <= ahoraMismo: 
            # si ya entro regresa al estado inicial del residente (N) y recalculo tiempos de E/S, punto salida, punto entrada
            tablaPlacasTiempos[idx][1] = ahoraMismo + datetime.timedelta(seconds=random.randint(rangoInfSegS,rangiSupSegS)
            tablaPlacasTiempos[idx][2] = tablaPlacasTiempos[idx][1] + datetime.timedelta(seconds=random.randint(rangoInfSegS,rangiSupSegS)
            tablaPlacasTiempos[idx][3] = 'N'
            tablaPlacasTiempos[idx][4], tablaPlacasTiempos[idx][5] = random.randint(1,4), random.randint(1,4)
            
except KeyboardInterrupt: # levanta una interrupción con CTRL-C
    pass
