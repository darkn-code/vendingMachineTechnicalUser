import RPi.GPIO as GPIO
import time 
import serial
from threading import Thread

port = '/dev/ttyUSB1'
baudRate = 115200
numero = '"5537950046"'
comando_habilitar_sms = 'AT+CMGF=1\r'
comandos_sms = 'AT+CMGS=' + numero + '\r' 
isRun = True

def leerDatosSerial():
    global isRun,sms
    time.sleep(1)
    while isRun:
        datos = sms.readline()
        datos = datos.decode('utf-8',errors='replace')
        print(datos)

def main():
    global sms
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.IN)
    sms = serial.Serial()
    sms.port = port
    sms.baudRarte = baudRate
    sms.open()
    time.sleep(1)
    sms.write(comando_habilitar_sms.encode())
    leerDatos = Thread(target=leerDatosSerial)
    leerDatos.start()
    while True:
        if GPIO.input(16):
            mensaje = 'Se no activo el sensor'
            print(mensaje)
            time.sleep(0.1)
        else:
            mensaje = '"Se activo el sensor"'
            print(comandos_sms)
            sms.write(comandos_sms.encode())
            time.sleep(3)
            sms.write(mensaje.encode())
            time.sleep(3)
            sms.write(bytes.fromhex('1A'))
            time.sleep(3)
            print('Sensor Activado')
            time.sleep(1)
    sms.close()


if __name__ == '__main__':
    main()
