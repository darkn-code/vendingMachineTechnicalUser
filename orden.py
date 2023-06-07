import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

conexionWin = 'ssh tablet-vending@192.168.1.3 "cd c:/proyecto-vending & '
path = './csv/{}'
pathhOrden = path.format('orden.csv')
pathListaPrecio = path.format('listaPrecio.csv')
isConnectBaseDatos = True


def main():
    #leer csv de ordenes
    try:
        orden = pd.read_csv(pathhOrden)
    except:
        columnas = {
                "IdCompra":[],
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
        tempPizza = int(sys.argv[3])
    except:
        tempPizza = 1
    try:
        numPizza = int(sys.argv[1])
        pizza = precio.iloc[numPizza][0]
        if tempPizza:
            precioPizza = precio.iloc[numPizza][1]
        else:
            precioPizza = precio.iloc[numPizza][2]
    except:
        print("Se necesita colocar un numero valido dentro de la lista de precio")
        print(precio)
        quit()
    try:
        cantidad = int(sys.argv[2])
    except:
        cantidad = 1
    try:
        idCompra = int(sys.argv[4])
    except:
        idCompra = -1
    total = precioPizza*cantidad
    now = datetime.now()
    nuevo_orden = {
            "IdCompra":[idCompra],
            "Descripcion":[pizza],
            "Cantidad":[cantidad],
            "Precio Unitario":[precioPizza],
            "Precio total":[total],
            "Temperatura Pizza" : [tempPizza],
            "Fecha" : [now.strftime("%d %m %y")],
            "Hora" : [now.strftime("%H:%M:%S")]
            }
    orden = pd.concat([orden, pd.DataFrame(nuevo_orden)], ignore_index=True)
    orden.to_csv('./csv/orden.csv',index=False)
    print(os.system(conexionWin+'echo "Orden Enviado">Recibido.txt"'))
    print(orden.tail(5))

if __name__ == '__main__':
    main()
