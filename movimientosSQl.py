import mysql.connector
import time
import datetime
import json
import pandas as pd
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

def efectuarMovimiento(mydb,id,metodoPago):
    if metodoPago == 0:
        pago = 4
    else:
        pago = 1
    orden = pd.read_csv('./csv/orden.csv')
    ordenId = orden[orden['IdCompra']==id]
    ordenSubTotal = ordenId.groupby(['Descripcion'])['Precio total'].sum()
    ordenCantidad = ordenId.groupby(['Descripcion'])['Descripcion'].count()

    total = int(ordenSubTotal.sum())


    mycursor = mydb.cursor()
    ts = time.time()
    monto = float(total / 1.16)
    iva = total - monto
    valorMovimiento = crearValor(columnasMovimiento)
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

    sql = "INSERT INTO movimientos ({}) VALUES ({})".format(columnasMovimiento,valorMovimiento)
    val = (0, 1, pago, 1, timestamp, 0,  0, None, None, None, 0, monto,0, iva, total, 0, 0, 1, 0 , None, None)
    #6 es metodo de pago: 1 efectivo/ 4 credito
    mycursor.execute(sql, val)
    mydb.commit()

    idMovimiento = mycursor.lastrowid
    valorMovimientoDetalle = crearValor(colMovDetalle)
    print(ordenId)
    for index in ordenCantidad.index:
        sql = "INSERT INTO movimientosDetalle ({}) VALUES ({})".format(colMovDetalle,valorMovimientoDetalle)
        importe = float(ordenSubTotal[index] / ordenCantidad[index])
        montoImporte = float(importe / 1.16)
        monto = float(ordenSubTotal[index]  / 1.16)
        iva = float(ordenSubTotal[index]  - monto)
        val = (0, idMovimiento, 0, 0, int(ordenCantidad[index]), montoImporte , monto, 0, iva, None)
        mycursor.execute(sql, val)
        mydb.commit()
        
    print(mycursor.rowcount, "record inserted.")
    return idMovimiento


def verificarMovimiento(mycursor,idMovimiento):
    mycursor.execute(comando.format(idMovimiento))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return myresult




if __name__ == '__main__':
    print(credenciales)
    mydb = mysql.connector.connect(
            host= credenciales["host"],
            user = credenciales["user"],
            password = credenciales["password"],
            database = credenciales["database"]
            )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM movimientos")
    mybase = mycursor.fetchall()
    idMovimiento = int(mybase[len(mybase) - 1][0])
    print(idMovimiento)
    idMovimiento = efectuarMovimiento(mydb,58,0)
    print(verificarMovimiento(mycursor,idMovimiento))
