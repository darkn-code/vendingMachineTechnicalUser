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
            escribirJson("codigoCredito",arrayString)
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
    monto_depositado = funciones.monto_depositado
    #monto_depositado = 100
    monto = leerJson("monto")
    codigoArray = leerJson("codigoCredito").split(',')
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
    os.system(conexionWin.format('csv/baseDatos.csv'))
    base = crearArray()
    response = make_response(json.dumps(base))
    response.content_type = 'application/json'
    return response


@app.route('/compraCancelada/<monto>')
def compraCancelada(monto):
    funciones.isRun = False
    #cerrarComunicacion()
    escribirJson("codigoCredito",'0,0')
    if monto == '0':
        validarCodigo = 0
        codigo = '' 
        return render_template('index.html')     
    else:
        validarCodigo = 1
        codigoGenerado = genearCodigo(monto,7)
        leerCodigo = pd.read_csv(pathOrden.format('codigoCredito.csv'))
        leerCodigo = pd.concat([leerCodigo,codigoGenerado],ignore_index=True)
        leerCodigo.to_csv(pathOrden.format('codigoCredito.csv'),index=False)
        codigo = codigoGenerado.loc[0,'codigo']
    context = {
        'codigo' : codigo,
        'validarCodigo' : validarCodigo
    }
    print('Validar Codigo:',validarCodigo)
    return render_template('cancelado.html',**context)


@app.route('/')
def index():
    funciones.isRun = False
    #cerrarComunicacion()
    response = make_response(render_template('index.html'))
    cookies = request.cookies
    for cookie in cookies:
        response.delete_cookie(cookie)
    return response

@app.route('/main')
def main():
    os.system(conexionWin.format('csv/baseDatos.csv'))
    os.system(conexionWin.format('csv/listaPrecio.csv'))
    funciones.isRun = False
    os.system("echo '1-1.4' | sudo tee /sys/bus/usb/drivers/usb/unbind")
    contadorArray = crearArray()
   
    context={'precioPizza':listaPizza['precio'],
             'precioPizzaFria':listaPizza['precioFria'],
             'nombreDePizza':listaPizza['vacio'],
             'lenPizza':len(listaPizza),
             } 
    idCompra = generarIDCompra()
    escribirJson("idCompra",idCompra)
    return render_template('main.html',**context)

@app.route('/enviarPeticion')
def enviarPeticion():
    global nombreDePizza
    cantidad = request.cookies.get("cantidad")
    cantidadFria = request.cookies.get("cantidadFria")
    monto = request.cookies.get("monto")
    print(cantidad)
    print(monto)
    thread = Thread(target=cobrarMonto, args=(int(monto),))
    thread.start()
    tempPizza = request.cookies.get("tempPizza")
    cantidadArray = cantidad.split(',')
    numPizza = sacarPizzas(cantidadArray)
    if numPizza == -1:
        print("pizza frias!")
        cantidadArray = cantidadFria.split(',')
        numPizza = sacarPizzas(cantidadArray)
        tempPizza = 0
        if numPizza == -1:
            return redirect(url_for('index'))
        
    idCompra = leerJson("idCompra")
    print('python3 orden.py {} {} {} {}'.format(numPizza,1,tempPizza,idCompra))
    #response = make_response([numPizza])
    escribirJson("cantidad",cantidad)
    escribirJson("cantidadFria",cantidadFria)
    escribirJson("numPizza",numPizza)
    escribirJson("tempPizza",tempPizza)
    escribirJson("monto",int(monto))
    return monto

@app.route('/mostarPagina')
def pagina():
    time.sleep(0.2)
    metodoPago = int(request.cookies.get("metodoPago"))
    codigoCredito = 0
    if metodoPago == 2:
        metodoPago = 1
        codigoCredito = 1
   
    tempPizza = int(leerJson("tempPizza"))
    monto = leerJson("monto")
    cantidadArray = leerJson("cantidad").split(',')
    cantidadFriaArray = leerJson("cantidadFria").split(',')

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
   
    numero = int(leerJson("numPizza"))
    if tempPizza:
        cantidadArray[numero] = str(int(cantidadArray[numero]) - 1)
        cantidad =','.join(cantidadArray)
        escribirJson("cantidad",cantidad)
    else:
        cantidadFriaArray[numero] = str(int(cantidadFriaArray[numero]) - 1)
        cantidad =','.join(cantidadFriaArray)
        escribirJson("cantidadFria",cantidad)

    context={
        'precioPizza' : precioPizza,
        'nombreDePizza' : nombreDePizza,
        'cantidadPizza' : cantidadPizza,
        'lenPizza':len(precioPizza),
        'subTotal' : subTotal,
        'monto' : monto,
        'metodoPago' : metodoPago,
        'codigoCredito' : codigoCredito
             }
    return render_template('pago.html',**context)

@app.route('/mandarAlPLC')
def mandarPLC():
    idCompra = int(leerJson("idCompra"))
    tempPizza = int(leerJson("tempPizza"))
    numero = int(leerJson("numPizza"))

    print('python3 orden.py {} {} {} {}'.format(numero,1,tempPizza,idCompra))
    os.system('python3 orden.py {} {} {} {}'.format(numero,1,tempPizza, idCompra))
    return render_template('horneando.html')

@app.route('/pizzaTerminada',methods=['GET'])
def pizzaTerminada():
    while True:
        status = open(pathConf.format("status.txt"),mode='r')
        status = status.read()
        tempPizza = int(leerJson("tempPizza"))
        print(status)
        if status.strip() == "Pizza":
            if tempPizza:
                cantidadArray = leerJson("cantidad").split(',')
            else:
                cantidadArray = leerJson("cantidadFria").split(',')
            print(leerJson("cantidad"))
            i = sacarPizzas(cantidadArray)
            if i == -1:
                if tempPizza:
                    print("pizza frias!")
                    tempPizza = 0
                    response = make_response(redirect(url_for('pizzaTerminada')))
                    escribirJson("tempPizza",tempPizza)
                    return response
                else:
                    print('Lista la pizza')
                    monto = float(leerJson("monto"))
                    threadSQL = Thread(target=enviarBaseDatos, args=(monto,))
                    threadSQL.start()
                    codigoArray = leerJson("codigoCredito").split(',')
                    isCodigo = int(codigoArray[0])
                    leerCodigo = pd.read_csv(pathOrden.format('codigoCredito.csv'))
                    codigo = leerCodigo.loc[int(codigoArray[1]),'codigo']
                    if isCodigo:
                        for index,row in leerCodigo.iterrows():
                            if (codigo == row['codigo']):
                                leerCodigo = leerCodigo.drop(index).reset_index(drop=True)
                                leerCodigo.to_csv(pathOrden.format('codigoCredito.csv'),index=False)
                            arrayString = '0,0'
                            escribirJson("codigoCredito",arrayString)
                            print(leerCodigo)
                    idCompra = int(leerJson("idCompra"))
                    content = {
                            'idCompra' : idCompra
                    }
                    return render_template('volver.html',**content)
                    break
            cantidadArray[i] = str(int(cantidadArray[i]) - 1)
            cantidad =','.join(cantidadArray)
            print(i)
            escribirJson("numPizza",i)
            if tempPizza:
                escribirJson("cantidad",cantidad)      
            else:
                escribirJson("cantidadFria",cantidad.strip())
            time.sleep(1)
            print(cantidad)
            return redirect(url_for('mandarPLC'))
        else:
            print(status)
            
if __name__ == '__main__':
    os.environ['FLASK_DEBUG'] = 'development'
    app.run(debug=True)
