from flask import Flask, render_template
import os


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)
