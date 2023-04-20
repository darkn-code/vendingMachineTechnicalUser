import pandas as pd
import numpy as np 
import time
import os
import mysql.connector
from mdbSerial import *
from movimientosSQl import *

""""Comandos para el billetero y monedero """
HABILITAR_MONEDERO = '0CFFFFFFFF'
DESHANILITAR_MONEDERO = '08'
CANTIDAD_MONDERO = '0A'
HABILITAR_BILLETERO = '34FFFFFFFF' 
ACEPTAR_BILLETE = '3501'
RECHAZAR_BILLETE = '3500'
RESETEAR_BILLETERO = '30'

BILLETE_20 = '30 90 09'
BILLETE_50 = '30 91 09'
BILLETE_100 = '30 92 09'
BILLETE_200 = '30 93 09'
BILLETE_500 = '30 94 09'

MONEDA_1 = '08 52'
MONEDA_5 = '08 54'
MONEDA_10 = '08 55'

DISNPESAR_MONEDAS_1 = '0D12'
DISNPESAR_MONEDAS_5 = '0D14'
DISNPESAR_MONEDAS_10 = '0D15'

""""Fin Comandos"""
PORT = '/dev/ttyUSB0'

isRun = True
monto_depositado = 0
listaPizza = pd.read_csv('./csv/listaPrecio.csv')
pathConf = './config/{}'


def leerArray(array):
    leer = open(pathConf.format(array),mode='r')
    arrayLeido = leer.read()
    leer.close()
    return arrayLeido.split(',')

def leertxt(texto):
    leer = open(pathConf.format(texto),mode='r')
    textoleido = int(leer.read())
    leer.close()
    return textoleido

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

def leer_cantidad_monedas(mdb):
    time.sleep(0.1)
    mdb.enviarDatos(CANTIDAD_MONDERO)
    leerDatosMdb = mdb.recibirDatos()
    leerDatosMdb = leerDatosMdb.decode('utf-8',errors='replace')
    leerDatosMdb = leerDatosMdb.strip()
    print(leerDatosMdb)
    Cantidad_total_1 = int(leerDatosMdb[12:14],16)
    Cantidad_total_5 = int(leerDatosMdb[18:20],16)
    Cantidad_total_10 = int(leerDatosMdb[21:23],16)
    Cantidad_total = Cantidad_total_1*1 + Cantidad_total_5*5 + Cantidad_total_10*10
    print(Cantidad_total) 


def enviarBaseDatos(monto):
    mydb = mysql.connector.connect(
            host= credenciales["host"],
            user = credenciales["user"],
            password = credenciales["password"],
            database = credenciales["database"]
            )
    mycursor = mydb.cursor()
    idMovimiento = efectuarMovimiento(mydb,monto)
    verificarMovimiento(mycursor,idMovimiento)

def cobrarMonto(monto):
    global isRun,monto_depositado 
    isRun = True
    monto_depositado = 0
    #monto = listaPizza['precio'][monto]
    print(monto)
        #os.system("echo '1-1.4' | sudo tee /sys/bus/usb/drivers/usb/bind")
    time.sleep(1.0)
    try:
        mdb = mdbSerial(PORT)
    except:
        mdb = mdbSerial('/dev/ttyUSB5')
    mdb.enviarDatos(HABILITAR_MONEDERO)
    time.sleep(0.1)
    mdb.enviarDatos(HABILITAR_BILLETERO)
    time.sleep(0.1)
    mdb.reinicarBuffer()
    while isRun:
        #monto_depositado+=10
        #time.sleep(1)
        leerDinero = mdb.recibirDatos()
        leerDinero = leerDinero.decode('utf-8',errors='replace')
        leerDinero = leerDinero.strip()
        print(leerDinero)
        #Monedas
        if leerDinero[:5] == MONEDA_1:
            monto_depositado+=1
        if leerDinero[:5] == MONEDA_5:
            monto_depositado+=5
        if leerDinero[:5] == MONEDA_10:
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
        print(leerDinero[:5]) 
        if (monto_depositado >= monto):
            #leer_cantidad_monedas(mdb)
            cambio = monto_depositado - monto
            print('Cambio: '+str(cambio))
            if (cambio != 0 ):
                time.sleep(0.5)
                cantidad_10 = cambio // 10
                cantidad_5 = (cambio % 10) // 5
                cantidad_1 = ((cambio % 10) % 5) // 1
                for i in range(cantidad_10):
                    mdb.enviarDatos(DISNPESAR_MONEDAS_10)
                    time.sleep(0.3)
                for i in range(cantidad_5):
                    mdb.enviarDatos(DISNPESAR_MONEDAS_5)
                    time.sleep(0.3)
                for i in range(cantidad_1):
                    mdb.enviarDatos(DISNPESAR_MONEDAS_1)
                    time.sleep(0.3)
            isRun = False
    time.sleep(1)
    mdb.enviarDatos(RESETEAR_BILLETERO)
    time.sleep(0.1)
    mdb.enviarDatos(DESHANILITAR_MONEDERO)
    time.sleep(0.1)
    mdb.mdbSerial.close()
    os.system('python3 verificarMonedero.py')
