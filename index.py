from flask import Flask, render_template, request,  make_response
import os
import json
import pandas as pd
import time
from threading import Thread
import serial
from mdbSerial import *
from funciones import *
import funciones

conexionWin = 'scp tablet-vending@192.168.50.30:c:/proyecto-vending/{} ./csv/'
listaPizza = pd.read_csv('./csv/listaPrecio.csv')
thread = Thread()
app = Flask(__name__)

@app.route('/data',methods=['GET'])
def cobrar():
    global numeroPizza
    monto_depositado = funciones.monto_depositado
    leernumeroPizza = open("numeroPizza.txt",mode='r')
    numeroPizza = int(leernumeroPizza.read())
    numeroPizza = int(listaPizza['precio'][numeroPizza])
    print(numeroPizza)
    response = make_response(json.dumps([monto_depositado,numeroPizza]))
    response.content_type = 'application/json'
    return response

@app.route('/comprobarBotones',methods=['GET'])
def comprobar():
    #os.system(conexionWin.format('baseDatos.csv'))
    base = crearArray()
    response = make_response(json.dumps(base))
    response.content_type = 'application/json'
    return response

@app.route('/')
def main():
    #os.system(conexionWin.format('baseDatos.csv'))
    #os.system(conexionWin.format('listaPrecio.csv'))
    funciones.isRun = False
    os.system("echo 'bus-puerto.puerto' | sudo tee /sys/bus/usb/drivers/usb/unbind")
    contadorArray = crearArray()
    context={'precioPizza':listaPizza['precio'],
             'nombreDePizza':listaPizza['vacio'],
             'lenPizza':len(listaPizza),
             }
    return render_template('index.html',**context)

@app.route('/enviarPeticion/<numero>')
def opcion1(numero):
    global nombreDePizza
    thread = Thread(target=cobrarMonto, args=(int(numero),))
    thread.start()
    os.system('echo {} > numeroPizza.txt'.format(numero))
    print('python3 orden.py '+ numero)
    return numero

@app.route('/mostarPagina')
def pagina():
    time.sleep(0.2)
    leernumeroPizza = open("numeroPizza.txt",mode='r')
    numeroPizza = int(leernumeroPizza.read())
    context={'precioPizza':listaPizza['precio'][numeroPizza],
             'nombreDePizza':listaPizza['vacio'][numeroPizza],
             }
    return render_template('pago.html',**context)

@app.route('/mandarAlPLC')
def mandarPLC():
    leernumeroPizza = open("numeroPizza.txt",mode='r')
    numero = int(leernumeroPizza.read())
    print('python3 orden.py {}'.format(numero))
    os.system('python3 orden.py '+ str(numero))
    return render_template('volver.html')

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)
