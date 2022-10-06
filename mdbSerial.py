import serial
import time

class mdbSerial:
    def __init__(self,port,baudRate=9600):
        self.port = port
        self.baudRate = baudRate
        self.mdbSerial = serial.Serial(self.port,self.baudRate)
    
    def enviarDatos(self,datos):
        self.mdbSerial.write(bytes.fromhex(datos))

    def recibirDatos(self):
        return self.mdbSerial.readline()
    
    def reinicarBuffer(self):
        self.mdbSerial.reset_input_buffer()