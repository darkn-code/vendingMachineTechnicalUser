import mysql.connector
import time
import datetime
import json

columnasMovimiento = 'movIdMovimiento, movIdFranquicia, movIdMetodoPago, movIdTipoMovimiento, movFecha, movIdTipoFactura, movIdUsoCFDI, movIdOrdenCompra, movIdEmpleado, movIdProveedor, movIdCliente, movSubTotalImporte, movDescuentoImporte, movIvaImporte, movTotalImporte, movFacturado, movFacturaEnviada, movIdEstatus, movIdUsuarioCre, movIdUsuarioAct, movIdUsuarioEli'
colMovDetalle = 'mdtIdMovimientoDetalle, mdtIdMovimiento, mdtIdConceptoDetalle, mdtTipoCambio, mdtCantidad, mdtImporte, mdtSubtotal, mdtDescuento, mdtIva, mdtObservaciones'

comando = 'SELECT * FROM movimientos join movimientosDetalle on movimientos.movIdMovimiento = movimientosDetalle.mdtIdMovimiento where movIdMovimiento = {}'

leerCredenciales = open("./config/credenciales.json",mode='r')
credenciales = json.load(leerCredenciales)
leerCredenciales.close()

def crearValor(columna):
    num = len(columna.split(','))
    valor = '%s, ' * num
    return valor[0:len(valor) - 2]

def efectuarMovimiento(mydb,total):
    mycursor = mydb.cursor()
    ts = time.time()
    monto = total / 1.16
    iva = total - monto
    valorMovimiento = crearValor(columnasMovimiento)
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

    sql = "INSERT INTO movimientos ({}) VALUES ({})".format(columnasMovimiento,valorMovimiento)
    val = (0, 1, 6, 1, timestamp, 0,  0, None, None, None, 0, monto,0, iva, total, 0, 0, 1, 0 , None, None)
    mycursor.execute(sql, val)
    mydb.commit()

    idMovimiento = mycursor.lastrowid
    valorMovimientoDetalle = crearValor(colMovDetalle)

    sql = "INSERT INTO movimientosDetalle ({}) VALUES ({})".format(colMovDetalle,valorMovimientoDetalle)
    val = (0, idMovimiento, 0, 0, 1, monto, monto, 0, iva, None)
    mycursor.execute(sql, val)
    mydb.commit()
    
    print(mycursor.rowcount, "record inserted.")
    return idMovimiento


def verificarMovimiento(mycursor,idMovimiento):
    mycursor.execute(comando.format(idMovimiento))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return myresult[0][0]


if __name__ == '__main__':
    print(credenciales)
    mydb = mysql.connector.connect(
            host= credenciales["host"],
            user = credenciales["user"],
            password = credenciales["password"],
            database = credenciales["database"]
            )
    mycursor = mydb.cursor()
    idMovimiento = efectuarMovimiento(mydb,99.0)
    print(verificarMovimiento(mycursor,idMovimiento))
