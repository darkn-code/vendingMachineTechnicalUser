import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
#from moviemientosSQl import efectuarMovimiento
#from moviemientosSQl import verificarMovimiento
#import mysql.connector

conexionWin = 'ssh tablet-vending@192.168.1.3 "cd c:/proyecto-vending & '
path = './csv/{}'
pathhOrden = path.format('orden.csv')
pathListaPrecio = path.format('listaPrecio.csv')
isConnectBaseDatos = True


def main():
    #try:
     #   mydb = mysql.connector.connect(
      #      host="50.62.182.151",
       #     user="remoteusr",
        #    password="remC0n€x1on",
         #   database="iBetelsa")
        #mycursor = mydb.cursor()
        #isConnectBaseDatos = True
    #except:
        #isConnectBaseDatos = False
        #print("no hay conexion a la base de datos")
    #leer csv de ordenes
    try:
        orden = pd.read_csv(pathhOrden)
    except:
        columnas = {
                "Descripcion":[],
                "Cantidad":[],
                "Precio Unitario":[],
                "Precio total":[],
                "Temperatura Pizza" : [],
                "Fecha": [],
                "Hora" : []
                }
        orden = pd.DataFrame(columnas)
    precio = pd.read_csv(pathListaPrecio)
    try:
        numPizza = int(sys.argv[1])
        pizza = precio.iloc[numPizza][0]
        precioPizza = precio.iloc[numPizza][1]
    except:
        print("Se necesita colocar un numero valido dentro de la lista de precio")
        print(precio)
        quit()
    try:
        cantidad = int(sys.argv[2])
    except:
        cantidad = 1
    try:
        tempPizza = int(sys.argv[3])
    except:
        tempPizza = 1
    total = precioPizza*cantidad
    now = datetime.now()
    nuevo_orden = {
            "Descripcion":pizza,
            "Cantidad":cantidad,
            "Precio Unitario":precioPizza,
            "Precio total":total,
            "Temperatura Pizza" : tempPizza,
            "Fecha" : now.strftime("%d %m %y"),
            "Hora" : now.strftime("%H:%M:%S")
            }
    #if isConnectBaseDatos:
     #   idMovimiento = efectuarMovimiento(mydb,float(total))
     #   verificarMovimiento(mycursor, idMovimiento)
    orden=orden.append(nuevo_orden,ignore_index=True)
    orden.to_csv('./csv/orden.csv',index=False)
    print(os.system(conexionWin+'echo "Orden Enviado">Recibido.txt"'))
    print(orden.tail(5))



if __name__ == '__main__':
    main()
