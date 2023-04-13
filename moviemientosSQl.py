import mysql.connector
import time
import datetime

columnasMovimiento = 'movIdMovimiento, movIdFranquicia, movIdMetodoPago, movIdTipoMovimiento, movFecha, movIdTipoFactura, movIdUsoCFDI, movIdOrdenCompra, movIdEmpleado, movIdProveedor, movIdCliente, movSubTotalImporte, movDescuentoImporte, movIvaImporte, movTotalImporte, movFacturaEnviada, movIdEstatus, movIdUsuarioCre, movIdUsuarioAct, movIdUsuarioEli'
numColumnaMov = len(columnasMovimiento.split(','))
valorMovimiento = '%s, ' * numColumnaMov
valorMovimiento = valorMovimiento[0:len(valorMovimiento) - 2]
colMovDetalle = 'mdtIdMovimientoDetalle, mdtIdMovimiento, mdtIdConceptoDetalle, mdtTipoCambio, mdtCantidad, mdtImporte, mdtSubtotal, mdtDescuento, mdtIva, mdtObservaciones'
numColMovDetalle = len(colMovDetalle.split(','))
valorMovimientoDetalle = '%s, ' * numColMovDetalle
valorMovimientoDetalle = valorMovimientoDetalle[0:len(valorMovimientoDetalle) - 2]

comando = 'SELECT * FROM movimientos join movimientosDetalle on movimientos.movIdMovimiento = movimientosDetalle.mdtIdMovimiento where movIdMovimiento = {}'

def efectuarMovimiento(mydb,total):
    mycursor = mydb.cursor()
    ts = time.time()
    monto = total / 1.16
    iva = total - monto
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    sql = "INSERT INTO movimientos ({}) VALUES ({})".format(columnasMovimiento,valorMovimiento)
    val = (0, 1, 1, 1, timestamp, 0,  0, None, None, None, 0, monto,0, iva, total, 0, 1, 0 , None, None)
    mycursor.execute(sql, val)
    mydb.commit()

    idMovimiento = mycursor.lastrowid

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


if __name__ == '__main__':
    mydb = mysql.connector.connect(
            host="50.62.182.151",
            user="remoteusr",
            password="remC0n€x1on",
            database="iBetelsa")
    mycursor = mydb.cursor()
    idMovimiento = efectuarMovimiento(mydb,99)
    verificarMovimiento(mycursor,idMovimiento)
