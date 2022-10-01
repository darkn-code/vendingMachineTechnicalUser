from flask import Flask, render_template
import os
import pandas as pd


app = Flask(__name__)

def contando(array,pizza):
    contador = 0
    for data in array:
        if data == pizza:
            contador+=1
    return contador


@app.route('/')
def main():
    listaPizza = pd.read_csv('./csv/listaPrecio.csv')
    baseDatos = pd.read_csv('./csv/baseDatos.csv')
    contadorArray = []
    print(baseDatos)
    print(listaPizza['vacio'])
    arrayA = baseDatos['A'].to_numpy()
    arrayB = baseDatos['B'].to_numpy()
    for pizza in listaPizza['vacio']:
        contador = contando(arrayA,pizza) + contando(arrayB,pizza)
        contadorArray.append(contador)
        contador=0

    print(contadorArray)
            

    return render_template('index.html',pizza=contadorArray,pizza10=listaPizza['vacio'])

@app.route('/opcion1/')
def opcion1():
    os.system('python3 orden.py 0')
    return render_template('volver.html')

@app.route('/opcion2/')
def opcion2():
    os.system('python3 orden.py 1')
    return render_template('volver.html')

@app.route('/opcion3/')
def opcion3():
    os.system('python3 orden.py 2')
    return render_template('volver.html')

@app.route('/opcion4/')
def opcion4():
    os.system('python3 orden.py 3')
    return render_template('volver.html')

@app.route('/opcion5/')
def opcion5():
    os.system('python3 orden.py 4')
    return render_template('volver.html')

@app.route('/opcion6/')
def opcion6():
    os.system('python3 orden.py 5')
    return render_template('volver.html')

@app.route('/opcion7/')
def opcion7():
    os.system('python3 orden.py 6')
    return render_template('volver.html')

@app.route('/opcion8/')
def opcion8():
    os.system('python3 orden.py 7')
    return render_template('volver.html')

if __name__ == '__main__':
    app.run(debug=True)
