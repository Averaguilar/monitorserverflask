# Augusto Vera y Aguilar, 12 de Mayo 2017
# Generador de movimientos de placas de residentes de Apodaca.

import urllib.request
import time
import random
import pyodbc
import datetime

# cuantas placas para la simulación y el intervalo inf y superior de delta en segundos de salidas y entradas.
placasEnMuestra = 100
municipio = "'APODACA'"
puntosSP = ['LAZARO CARDENAS', 'CALZADA SAN PEDRO', 'AVE HUMBERTO LOBO', 'SANTA BARBARA']
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=AUGUSTO-LENOVO\SQLEXPRESS;DATABASE=MONITORPLACAS')
cursor = cnxn.cursor()
# ejecuto el cursor que saca la muestra de placas para la simulación.
cursor.execute("SELECT DISTINCT TOP "+ str(placasEnMuestra) + " Id, PLACAS FROM PADRON_PLACAS_NL WHERE MUNICIPIO=" + municipio + "AND PLACAS IS NOT NULL")
muestraPlacasSP =  cursor.fetchall()
# creo el diccionario interno de placas en movimiento
dicPlacasMuestra = {muestraPlacasSP[i][0] : [muestraPlacasSP[i][1],'S'] for i in range(placasEnMuestra)}
# {100: ['sdf1234', 'N']}
# [0..len][0,1]
print("Muestra de placas > ", dicPlacasMuestra)
cursor.execute("SELECT * FROM CATALOGO_ACCESOS")
listAccesos =  cursor.fetchall()
catalogoAccesos = dict(listAccesos)
print("Catalogo accesos > ", catalogoAccesos)

try:
    while True:
        # ahora selecciono una placa aleatoria de la base de datos
        idxPlacaAleatorio = random.randint(muestraPlacasSP[0][0], muestraPlacasSP[len(dicPlacasMuestra)-1][0])
        ahoraMismo = str(datetime.datetime.now()).replace(' ','%20')
        # veo si la placa ya está en la muestra para marcar su regreso.
        if dicPlacasMuestra[idxPlacaAleatorio][1] == 'S' and bool(random.getrandbits(1)): 
            puntoAcceso = random.randint(1,4)
            urlstring = 'http://127.0.0.1:8080/enviaplaca/{}/{}/{}/{}'.format(dicPlacasMuestra[idxPlacaAleatorio][0], str(ahoraMismo), 'E', puntoAcceso)
            with urllib.request.urlopen(urlstring) as f:
                print(f.read(300).decode('utf-8'))
            dicPlacasMuestra[idxPlacaAleatorio][1] = 'E'
            print("salió la placa: <{}> por el punto: <{}>".format(dicPlacasMuestra[idxPlacaAleatorio][0], catalogoAccesos[puntoAcceso])) 
        # vuelvo a seleccionar una placa aleatoria
        idxPlacaAleatorio = random.randint(muestraPlacasSP[0][0], muestraPlacasSP[len(dicPlacasMuestra)-1][0])
        if dicPlacasMuestra[idxPlacaAleatorio][1] == 'E' and bool(random.getrandbits(1)):
            puntoAcceso = random.randint(1,4)
            urlstring = 'http://127.0.0.1:8080/enviaplaca/{}/{}/{}/{}'.format(dicPlacasMuestra[idxPlacaAleatorio][0], str(ahoraMismo), 'S', puntoAcceso)
            with urllib.request.urlopen(urlstring) as f:
                print(f.read(300).decode('utf-8'))
            dicPlacasMuestra[idxPlacaAleatorio][1] = 'S'
            print("entró la placa: <{}> por el punto: <{}>".format(dicPlacasMuestra[idxPlacaAleatorio][0], catalogoAccesos[puntoAcceso])) 
        time.sleep(random.randint(1,5))    
except KeyboardInterrupt: # levanta una interrupción con CTRL-C
    pass
