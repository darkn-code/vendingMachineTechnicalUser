from flask import Flask, render_template, request,  make_response, redirect, url_for
import os
import json
import pandas as pd
import time
import numpy as np
from threading import Thread
import serial
from mdbSerial import *
from funciones import *
import funciones

conexionWin = 'scp tablet-vending@192.168.1.3:c:/proyecto-vending/{} ./csv/'
listaPizza = pd.read_csv('./csv/listaPrecio.csv')
pathConf = './config/{}'
pathOrden = './csv/{}'
thread = Thread()
app = Flask(__name__)


@app.route('/verificarCodigo/<codigo>',methods=['GET'])
def verificarCodigo(codigo):
    leerCodigo = pd.read_csv(pathOrden.format('codigoCredito.csv'))
    #arrayCodigo = leerCodigo.loc[:,'codigo']
    for index,row in leerCodigo.iterrows():
        if (codigo == row['codigo']):
            print('Codigo Encontrado')
            array = ['1',str(index)]
            arrayString =','.join(array)
            os.system('echo {} > {}'.format(arrayString,pathConf.format("codigoCredito.txt")))
            response = make_response(json.dumps([1]))
            response.content_type = 'application/json'
            return response 
    print("Codigo no encontrado")
    response = make_response(json.dumps([0]))
    response.content_type = 'application/json'
    return response

@app.route('/data',methods=['GET'])
def cobrar():
    global numeroPizza
    #monto_depositado = funciones.monto_depositado
    monto_depositado = 80
    monto = leertxt("monto.txt")
    codigoArray = leerArray("codigoCredito.txt")
    isCodigo = int(codigoArray[0])
    if isCodigo:
        leerCodigo = pd.read_csv(pathOrden.format('codigoCredito.csv'))
        codigoMonto = int(leerCodigo.loc[int(codigoArray[1]),'monto'])
        print(codigoMonto)
        monto_depositado += codigoMonto
    #numeroPizza = int(listaPizza['precio'][numeroPizza])
    print(monto_depositado)
    response = make_response(json.dumps([monto_depositado,monto]))
    response.content_type = 'application/json'
    return response

@app.route('/comprobarBotones',methods=['GET'])
def comprobar():
    #os.system(conexionWin.format('csv/baseDatos.csv'))
    base = crearArray()
    response = make_response(json.dumps(base))
    response.content_type = 'application/json'
    return response


@app.route('/compraCancelada/<monto>')
def compraCancelada(monto):
    codigoGenerado = genearCodigo(monto,7)
    leerCodigo = pd.read_csv(pathOrden.format('codigoCredito.csv'))
    leerCodigo = pd.concat([leerCodigo,codigoGenerado],ignore_index=True)
    leerCodigo.to_csv(pathOrden.format('codigoCredito.csv'),index=False)
    codigo = codigoGenerado.loc[0,'codigo']
    context = {
        'codigo' : codigo
    }
    return render_template('cancelado.html',**context)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main/<tempPizza>')
def main(tempPizza):
    os.system('echo {} > {}'.format(tempPizza,pathConf.format("tempPizza.txt")))
    #os.system(conexionWin.format('csv/baseDatos.csv'))
    #os.system(conexionWin.format('csv/listaPrecio.csv'))
    funciones.isRun = False
    #os.system("echo '1-1.4' | sudo tee /sys/bus/usb/drivers/usb/unbind")
    contadorArray = crearArray()
    context={'precioPizza':listaPizza['precio'],
             'precioPizzaFria':listaPizza['precioFria'],
             'nombreDePizza':listaPizza['vacio'],
             'lenPizza':len(listaPizza),
             }
    return render_template('main.html',**context)

@app.route('/enviarPeticion/<cantidad>/<cantidadFria>/<monto>')
def opcion1(cantidad,cantidadFria,monto):
    global nombreDePizza
    #thread = Thread(target=cobrarMonto, args=(int(monto),))
    #thread.start()
    os.system('echo {} > {}'.format(cantidad,pathConf.format("cantidad.txt")))
    os.system('echo {} > {}'.format(cantidadFria,pathConf.format("cantidadFria.txt")))
    os.system('echo {} > {}'.format(monto,pathConf.format("monto.txt")))
    tempPizza = leertxt("tempPizza.txt")
    cantidadArray = cantidad.split(',')
    print(len(cantidadArray))
    i = 0
    while int(cantidadArray[i]) == 0:
        i +=1
        if i == len(cantidadArray):
            print("pizza frias!")
            if not tempPizza:
                return render_template('volver.html')
            os.system('echo {} > {}'.format(0,pathConf.format("tempPizza.txt")))
            cantidadArray = cantidadFria.split(',')
            i = 0
    os.system('echo {} > {}'.format(i,pathConf.format("numeroPizza.txt")))
    try:
        orden = pd.read_csv(pathOrden.format('orden.csv'))
        idCompra = int(orden.loc[len(orden)-1,'IdCompra'])
        #idCompra = int(open(pathConf.format("idCompra.txt"),mode='r').read())
    except:
        os.system('echo {} > {}'.format(0,pathConf.format("idCompra.txt")))
    idCompra += 1
    os.system('echo {} > {}'.format(idCompra,pathConf.format("idCompra.txt")))
    print('python3 orden.py {} {} {} {}'.format(i,1,tempPizza,idCompra))
    return monto

@app.route('/mostarPagina/<metodoPago>')
def pagina(metodoPago):
    time.sleep(0.2)
    leertempPizza = open(pathConf.format("tempPizza.txt"),mode='r')
    tempPizza = int(leertempPizza.read())
    cantidadArray = leerArray("cantidad.txt")
    cantidadFriaArray = leerArray("cantidadFria.txt")
    monto = leertxt("monto.txt")
    nombreDePizza = []
    precioPizza = []
    cantidadPizza = []
    subTotal = []
   
    for i in range(len(cantidadArray)):
        if int(cantidadArray[i]) != 0:
             precioPizza.append(listaPizza['precio'][i])
             nombreDePizza.append(listaPizza['vacio'][i])
             cantidadPizza.append(cantidadArray[i])
             subTotal.append(int(listaPizza['precio'][i]) * int(cantidadArray[i]))
        if int(cantidadFriaArray[i]) != 0:
             precioPizza.append(listaPizza['precioFria'][i])
             nombreDePizza.append(listaPizza['vacio'][i]+' Congelada')
             cantidadPizza.append(cantidadFriaArray[i])
             subTotal.append(int(listaPizza['precioFria'][i]) * int(cantidadFriaArray[i]))

    numero = leertxt("numeroPizza.txt")
    if tempPizza:
        cantidadArray[numero] = str(int(cantidadArray[numero]) - 1)
        cantidad =','.join(cantidadArray)
        os.system('echo {} > {}'.format(cantidad.strip(),pathConf.format("cantidad.txt")))
    else:
        cantidadFriaArray[numero] = str(int(cantidadFriaArray[numero]) - 1)
        cantidad =','.join(cantidadFriaArray)
        os.system('echo {} > {}'.format(cantidad.strip(),pathConf.format("cantidadFria.txt")))
    context={
        'precioPizza' : precioPizza,
        'nombreDePizza' : nombreDePizza,
        'cantidadPizza' : cantidadPizza,
        'lenPizza':len(precioPizza),
        'subTotal' : subTotal,
        'monto' : monto,
        'metodoPago' : int(metodoPago)
             }
    
    return render_template('pago.html',**context)

@app.route('/mandarAlPLC')
def mandarPLC():
    idCompra = leertxt("idCompra.txt")
    tempPizza = leertxt("tempPizza.txt")
    numero = leertxt("numeroPizza.txt")
    print('python3 orden.py {} {} {} {}'.format(numero,1,tempPizza,idCompra))
    os.system('python orden.py {} {} {} {}'.format(numero,1,tempPizza, idCompra))
    return render_template('horneando.html')

@app.route('/pizzaTerminada',methods=['GET'])
def pizzaTerminada():
    while True:
        status = open(pathConf.format("status.txt"),mode='r')
        status = status.read()
        tempPizza = leertxt("tempPizza.txt")
        if status.strip() == "Pizza":
            if tempPizza:
                cantidadArray = leerArray("cantidad.txt")
            else:
                cantidadArray = leerArray("cantidadFria.txt")
            i = 0
            while int(cantidadArray[i]) == 0:
                i +=1
                if i == len(cantidadArray):
                    if tempPizza:
                        print("pizza frias!")
                        os.system('echo {} > {}'.format(0,pathConf.format("tempPizza.txt")))
                        return redirect(url_for('pizzaTerminada'))
                    else:
                        print('Lista la pizza')
                        monto = leertxt("monto.txt")
                        #threadSQL = Thread(target=enviarBaseDatos, args=(monto,))
                        #threadSQL.start()
                        codigoArray = leerArray("codigoCredito.txt")
                        isCodigo = int(codigoArray[0])
                        leerCodigo = pd.read_csv(pathOrden.format('codigoCredito.csv'))
                        codigo = leerCodigo.loc[int(codigoArray[1]),'codigo']
                        if isCodigo:
                            for index,row in leerCodigo.iterrows():
                                if (codigo == row['codigo']):
                                    leerCodigo = leerCodigo.drop(index).reset_index(drop=True)
                                    leerCodigo.to_csv(pathOrden.format('codigoCredito.csv'),index=False)
                            arrayString = '0,0'
                            os.system('echo {} > {}'.format(arrayString,pathConf.format("codigoCredito.txt")))
                            print(leerCodigo)
                        return render_template('volver.html')
                        break
            cantidadArray[i] = str(int(cantidadArray[i]) - 1)
            cantidad =','.join(cantidadArray)
            print(cantidadArray)
            os.system('echo {} > {}'.format(i,pathConf.format("numeroPizza.txt")))
            if tempPizza:
                os.system('echo {} > {}'.format(cantidad.strip(),pathConf.format("cantidad.txt")))
            else:
                os.system('echo {} > {}'.format(cantidad.strip(),pathConf.format("cantidadFria.txt")))
            return redirect(url_for('mandarPLC'))
        else:
            print(status)
            

if __name__ == '__main__':
    os.environ['FLASK_DEBUG'] = 'development'
    app.run(debug=True)
