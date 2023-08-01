import subprocess
import hashlib
import json

def obtener_numero_serie():
    cpuinfo = subprocess.check_output(['cat', '/proc/cpuinfo']).decode()
    
    for linea in cpuinfo.split('\n'):
        if linea.startswith('Serial'):
            numero_serie = linea.split(':')[1].strip()
            return numero_serie
    
    return None

def calcular_valor_hash(numero_serie, clave_secreta):
    cadena_a_hash = numero_serie + clave_secreta
    valor_hash = hashlib.sha256(cadena_a_hash.encode()).hexdigest()
    return valor_hash

def guardarHashJson():
    numero_serie = obtener_numero_serie()
    clave_secreta = 'tX459D#NM%VnjWR'
    dataHash = calcular_valor_hash(numero_serie,clave_secreta)

    with open('hash.json','w') as f:
        json.dump(dataHash,f)

def main():
    with open('./config/hash.json', 'r') as f:
        hashPermito = json.load(f)
    numero_serie_actual = obtener_numero_serie()
    clave_secreta = 'tX459D#NM%VnjWR'
    hashActual = calcular_valor_hash(numero_serie_actual,clave_secreta)


    if hashActual == hashPermito:
        print("Ejecutando el código en la Raspberry Pi permitida.")
    else:
        print("No estás utilizando la Raspberry Pi permitida.")






if __name__ == '__main__':
    main()




