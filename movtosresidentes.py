# Augusto Vera y Aguilar, 22 de Abril 2017
# primer ensayo de script python que llama a un servidor de web flask el servidor se llama Flaktest.py
# Puse el servidor prototipo de Flask (Flasktest.py) en la virtual de windows 7 virtualbox "python3.6 con flask"

import urllib.request
import time
import random
import pyodbc
import datetime

# cuantas placas para la simulación y el intervalo inf y superior de delta en segundos de salidas y entradas.
placasEnMuestra = 100
municipio = "'SAN PEDRO'"

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=AUGUSTO-LENOVO\SQLEXPRESS;DATABASE=MONITORPLACAS')
cursor = cnxn.cursor()
# ejecuto el cursor que saca la muestra de placas para la simulación.
cursor.execute("SELECT DISTINCT TOP "+ str(placasEnMuestra) + " Id, PLACAS FROM PADRON_PLACAS_NL WHERE MUNICIPIO=" + municipio)
muestraPlacasSP =  cursor.fetchall()
# creo el diccionario interno de placas en movimiento
dicPlacasMuestra = {muestraPlacasSP[i][0] : [muestraPlacasSP[i][1],'E'] for i in range(placasEnMuestra)}
# {100: ['sdf1234', 'N']}
# [0..len][0,1]
print(dicPlacasMuestra)

try:
    while True:
        # ahora selecciono una placa aleatoria de la base de datos
        idxPlacaAleatorio = random.randint(muestraPlacasSP[0][0], muestraPlacasSP[len(dicPlacasMuestra)-1][0])
        # cursor.execute("SELECT DISTINCT Id, PLACAS FROM PADRON_PLACAS_NL WHERE Id={}".format(str(random.randint(1, 1600000))))
        # dicPlacasMuestra =  cursor.fetchall()
        # print(dicPlacasMuestra)
        ahoraMismo = str(datetime.datetime.now()).replace(' ','%20')
        # veo si la placa ya está en la muestra para marcar su regreso.
        if dicPlacasMuestra[idxPlacaAleatorio][1] == 'E' and bool(random.getrandbits(1)): 
            urlstring = 'http://127.0.0.1:8080/enviaplaca/{}/{}/{}/{}'.format(dicPlacasMuestra[idxPlacaAleatorio][0], str(ahoraMismo), 'S', random.randint(1,4))
            with urllib.request.urlopen(urlstring) as f:
                print(f.read(300).decode('utf-8'))
            dicPlacasMuestra[idxPlacaAleatorio][1] = 'S'
            # print("URL --> " + urlstring)
            print("salio la placa ", dicPlacasMuestra[idxPlacaAleatorio][0]) 
        if dicPlacasMuestra[idxPlacaAleatorio][1] == 'S' and bool(random.getrandbits(1)):
            urlstring = 'http://127.0.0.1:8080/enviaplaca/{}/{}/{}/{}'.format(dicPlacasMuestra[idxPlacaAleatorio][0], str(ahoraMismo), 'E', random.randint(1,4))
            with urllib.request.urlopen(urlstring) as f:
                print(f.read(300).decode('utf-8'))
            dicPlacasMuestra[idxPlacaAleatorio][1] = 'E'
            # print("URL --> " + urlstring)
            print("entró la placa ", dicPlacasMuestra[idxPlacaAleatorio][0]) 
        time.sleep(random.randint(1,5))    
except KeyboardInterrupt: # levanta una interrupción con CTRL-C
    pass
