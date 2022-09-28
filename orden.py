import pandas as pd
import numpy as np
import os
import sys

conexionWin = 'ssh tablet-vending@192.168.50.30 "cd c:/proyecto-vending & '

def main():
    try:
        orden = pd.read_csv('orden.csv')
    except:
        columnas = {"Descripcion":[],"Cantidad":[],"Precio Unitario":[],
                "Precio total":[]}
        orden = pd.DataFrame(columnas)
    precio = pd.read_csv('listaPrecio.csv')
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
    total = precioPizza*cantidad
    nuevo_orden = {"Descripcion":pizza,"Cantidad":cantidad,"Precio Unitario":precioPizza,"Precio total":total}
    orden=orden.append(nuevo_orden,ignore_index=True)
    orden.to_csv('orden.csv',index=False)
    print(os.system(conexionWin+'echo "Orden Enviado">Recibido.txt"'))
    print(orden)



if __name__ == '__main__':
    main()
