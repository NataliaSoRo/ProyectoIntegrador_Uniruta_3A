from database.conexion import Conexion
from models.pago import Pago

class PagoDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
            
        cursor.execute("SELECT * FROM pago")
        registros = cursor.fetchall()

        pagos = []
        for registro in registros:

            pago = Pago(
                id_pago=registro[0],
                id_viaje=registro[1],
                id_chofer=registro[2],
                pago_base=registro[3],
                pago_final=registro[4],
                pago_inicial=registro[5],
                total_acumulado=registro[6],          
                metodo_pago=registro[7],
                periodo_pago=registro[8],
                )
            pagos.append(pago)
        cursor.close()
        conexion.close()

        return pagos
    
    def insertar(self, pago):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql ="""
        INSERT INTO pagos (id_pagos, id_chofer, pago_inicial, pago_final, pago_total_acumulado, metodo_pago, periodo_pago, pago_base)
        VALUES (%s, %s, %s, %s, %s, %s,%s, %s)
        """

        cursor.execute(
            sql,
            (pago.id_pagos,
            pago.id_chofer,
            pago.pago_inicial,
            pago.pago_final,
            pago.pago_total_acumulado,
            pago.metodo_pago,
            pago.periodo_pago,
            pago.pago_base)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        
    def actualizar(self, chofer):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql ="""
        UPDATE choferes
        SET nombre = %s, telefono = %s, licencia = %s, tipo_licencia = %s, vigen_licencia = %s, estatus = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (chofer.nombre,
            chofer.telefono,
            chofer.licencia,
            chofer.tipo_licencia,
            chofer.vigen_licencia,
            chofer.estatus,
            chofer.id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        
    def eliminar(self, chofer_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM choferes WHERE id = %s",
            (chofer_id,)
            )
        conexion.commit()
        cursor.close()
        conexion.close()
    
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_pagos FROM pagos ORDER BY id_pagos DESC")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]
    
