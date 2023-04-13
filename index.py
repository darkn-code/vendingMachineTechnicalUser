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
thread = Thread()
app = Flask(__name__)

@app.route('/data',methods=['GET'])
def cobrar():
    global numeroPizza
    monto_depositado = funciones.monto_depositado
    #monto_depositado = 400
    leermonto = open("monto.txt",mode='r')
    leercantidad = open("cantidad.txt",mode='r')
    cantidad = leercantidad.read()
    cantidadArray = cantidad.split(',')
    monto = int(leermonto.read())
    #numeroPizza = int(listaPizza['precio'][numeroPizza])
    print(cantidadArray)
    print(monto)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main/<tempPizza>')
def main(tempPizza):
    os.system('echo {} > tempPizza.txt'.format(tempPizza))
    os.system(conexionWin.format('csv/baseDatos.csv'))
    os.system(conexionWin.format('csv/listaPrecio.csv'))
    funciones.isRun = False
    #os.system("echo '1-1.4' | sudo tee /sys/bus/usb/drivers/usb/unbind")
    contadorArray = crearArray()
    context={'precioPizza':listaPizza['precio'],
             'nombreDePizza':listaPizza['vacio'],
             'lenPizza':len(listaPizza),
             }
    return render_template('main.html',**context)

@app.route('/enviarPeticion/<cantidad>/<monto>')
def opcion1(cantidad,monto):
    global nombreDePizza
    thread = Thread(target=cobrarMonto, args=(int(monto),))
    thread.start()
    os.system('echo {} > cantidad.txt'.format(cantidad))
    os.system('echo {} > monto.txt'.format(monto))
    tempPizza = open("tempPizza.txt",mode='r').read()
    cantidadArray = cantidad.split(',')
    i = 0
    while int(cantidadArray[i]) == 0:
        i +=1
    os.system('echo {} > numeroPizza.txt'.format(i))
    print('python3 orden.py {} {} {}'.format(cantidadArray[0],1,tempPizza))
    return monto

@app.route('/mostarPagina')
def pagina():
    time.sleep(0.2)
    leercantidad = open("cantidad.txt",mode='r')
    cantidad = leercantidad.read()
    cantidadArray = cantidad.split(',')
    leermonto = open("monto.txt",mode='r')
    nombreDePizza = []
    precioPizza = []
    cantidadPizza = []
    subTotal = []
    monto = int(leermonto.read())
    for i in range(len(cantidadArray)):
        if int(cantidadArray[i]) != 0:
             precioPizza.append(listaPizza['precio'][i])
             nombreDePizza.append(listaPizza['vacio'][i])
             cantidadPizza.append(cantidadArray[i])
             subTotal.append(int(listaPizza['precio'][i]) * int(cantidadArray[i]))

    leernumeroPizza = open("numeroPizza.txt",mode='r')
    numero = int(leernumeroPizza.read())
    cantidadArray[numero] = str(int(cantidadArray[numero]) - 1)
    cantidad =','.join(cantidadArray)
    #print('echo "{}" > cantidad.txt'.format(cantidad.strip()))
    os.system('echo {} > cantidad.txt'.format(cantidad.strip()))
    context={
        'precioPizza' : precioPizza,
        'nombreDePizza' : nombreDePizza,
        'cantidadPizza' : cantidadPizza,
        'lenPizza':len(precioPizza),
        'subTotal' : subTotal,
        'monto' : monto
             }
    
    return render_template('pago.html',**context)

@app.route('/mandarAlPLC')
def mandarPLC():
    leernumeroPizza = open("numeroPizza.txt",mode='r')
    leertempPizza = open("tempPizza.txt",mode='r')
    tempPizza = int(leertempPizza.read())
    numero = int(leernumeroPizza.read())
    print('python3 orden.py {} {} {}'.format(numero,1,tempPizza))
    os.system('python3 orden.py {} {} {}'.format(numero,1,tempPizza))
    return render_template('horneando.html')

@app.route('/pizzaTerminada',methods=['GET'])
def pizzaTerminada():
    while True:
        status = open("./csv/status.txt",mode='r')
        status = status.read()
        print(status.strip() == "Pizza")
        if status.strip() == "Pizza":
            leercantidad = open("cantidad.txt",mode='r')
            cantidad = leercantidad.read()
            cantidadArray = cantidad.split(',')
            print(cantidadArray)
            i = 0
            while int(cantidadArray[i]) == 0:
                i +=1
                if i == len(cantidadArray):
                    print('Lista la pizza')
                    return render_template('volver.html')
                    break
            cantidadArray[i] = str(int(cantidadArray[i]) - 1)
            cantidad =','.join(cantidadArray)
            print(cantidadArray)
            os.system('echo {} > numeroPizza.txt'.format(i))
            os.system('echo {} > cantidad.txt'.format(cantidad.strip()))
            return redirect(url_for('mandarPLC'))
            

    #else:
     #   print("pizza horneando")
      #  response = make_response(json.dumps([status]))
        #response.content_type = 'application/json'
        #return response  

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)
