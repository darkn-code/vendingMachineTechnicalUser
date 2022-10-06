import pandas as pd
import numpy as np 
import time
import os
from mdbSerial import *

""""Comandos para el billetero y monedero """
HABILITAR_MONEDERO = '0CFFFFFFFF'
DESHANILITAR_MONEDERO = '08'
HABILITAR_BILLETERO = '34FFFFFFFF' 
ACEPTAR_BILLETE = '3501'
RECHAZAR_BILLETE = '3500'
RESETEAR_BILLETERO = '30'

BILLETE_20 = '30 90 09'
BILLETE_50 = '30 91 09'
BILLETE_100 = '30 92 09'
BILLETE_200 = '30 93 09'
BILLETE_500 = '30 94 09'

MONEDA_1 = '08 52 00'
MONEDA_5 = '08 54 00'
MONEDA_10 = '08 55 00'
""""Fin Comandos"""
PORT = '/dev/ttyUSB0'

isRun = True
monto_depositado = 0
listaPizza = pd.read_csv('./csv/listaPrecio.csv')

def contando(array,pizza):
    contador = 0
    for data in array:
        if data == pizza:
            contador+=1
    return contador

def crearArray():
    baseDatos = pd.read_csv('./csv/baseDatos.csv')
    contadorArray = []
    arrayA = baseDatos['A'].to_numpy()
    arrayB = baseDatos['B'].to_numpy()
    for pizza in listaPizza['vacio']:
        contador = contando(arrayA,pizza) + contando(arrayB,pizza)
        contadorArray.append(contador)
        contador=0
    print(contadorArray)
    return contadorArray

def cobrarMonto(monto):
    global isRun,monto_depositado 
    isRun = True
    monto_depositado = 0
    time.sleep(1.0)
    print(monto)
    #os.system("echo 'bus-puerto.puerto' | sudo tee /sys/bus/usb/drivers/usb/bind")
    mdb = mdbSerial(PORT)
    mdb.enviarDatos(HABILITAR_MONEDERO)
    time.sleep(0.1)
    mdb.enviarDatos(HABILITAR_BILLETERO)
    time.sleep(0.1)
    #mdb.reiniciarBuffer()
    while isRun:
        leerDinero = mdb.recibirDatos()
        leerDinero = leerDinero.decode('utf-8',errors='replace')
        leerDinero = leerDinero.strip()
        print(leerDinero)
        #Monedas
        if leerDinero == MONEDA_1:
            monto_depositado+=1
        if leerDinero == MONEDA_5:
            monto_depositado+=5
        if leerDinero == MONEDA_10:
            monto_depositado+=10
        #Billetes
        if leerDinero == BILLETE_20:
            mdb.enviarDatos(ACEPTAR_BILLETE)
            monto_depositado+=20
        if leerDinero == BILLETE_50:
            mdb.enviarDatos(ACEPTAR_BILLETE)
            monto_depositado+=50
        if leerDinero == BILLETE_100:
            mdb.enviarDatos(ACEPTAR_BILLETE)
            monto_depositado+=100
        if leerDinero == BILLETE_200:
            mdb.enviarDatos(ACEPTAR_BILLETE)
            monto_depositado+=200
        if leerDinero == BILLETE_500:
            mdb.enviarDatos(ACEPTAR_BILLETE)
            monto_depositado+=500

        if (monto_depositado >= listaPizza['precio'][monto]):
            isRun = False
    time.sleep(1)
    mdb.enviarDatos(RESETEAR_BILLETERO)
    time.sleep(0.1)
    mdb.enviarDatos(DESHANILITAR_MONEDERO)
    time.sleep(0.1)
    mdb.mdbSerial.close() 





