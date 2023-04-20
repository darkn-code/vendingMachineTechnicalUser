from mdbSerial import *
from threading import Thread
import time
import pandas as pd


PORT = '/dev/ttyUSB{}'
CANTIDAD_MONDERO = '0A'
PATH = './csv/cantidadMonedas.csv'

def leerDatos():
    global mdb,isRun
    monedas = []
    while isRun:
        leerInformacion = mdb.recibirDatos()
        leerInformacion = leerInformacion.decode('utf-8',errors='replace')
        leerInformacion = leerInformacion.strip()
        print(leerInformacion)
        if len(leerInformacion) == 56:
            monedas.append(int(leerInformacion[12:14],16))
            monedas.append(int(leerInformacion[18:20],16))
            monedas.append(int(leerInformacion[21:23],16))
            print('Cantidad de monedas 1:{}, 5:{}, 10:{}'.format(monedas[0],monedas[1],monedas[2]))
            isRun = False
    columnas = ['Monedas 1','Monedas 5','Monedas 10']
    cantMonData = pd.DataFrame([monedas],columns=columnas)
    print(cantMonData)
    cantMonData.to_csv(PATH)



def main():
    global mdb,isRun
    isRun = True
    try:
        mdb = mdbSerial(PORT.format(0))
    except:
        mdb = mdbSerial(PORT.format(5))

    thread = Thread(target=leerDatos)
    thread.start()
    time.sleep(1)
    mdb.enviarDatos(CANTIDAD_MONDERO)


if __name__ == '__main__':
    main()
