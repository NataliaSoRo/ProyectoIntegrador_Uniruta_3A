from database.conexion import Conexion
from models.pago import Pago

class PagoDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        pagos = []
        try:
            query = """
                SELECT p.id, p.id_viaje, p.id_chofer, p.pago_base, p.pago_final, 
                       p.pago_inicial, p.total_acumulado, p.metodo_pago, p.periodo_pago,
                       c.nombre
                FROM pago p
                JOIN choferes c ON p.id_chofer = c.id
            """
            cursor.execute(query)
            registros = cursor.fetchall()

            for registro in registros:
                pago = Pago(
                    id=registro[0],
                    id_viaje=registro[1],
                    id_chofer=registro[2],
                    pago_base=registro[3],
                    pago_final=registro[4],
                    pago_inicial=registro[5],
                    total_acumulado=registro[6],
                    metodo_pago=registro[7],
                    periodo_pago=registro[8],
                    nombre_chofer=registro[9]
                )
                pagos.append(pago)
        finally:
            cursor.close()
            conexion.close()

        return pagos

    def insertar(self, pago):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """
                INSERT INTO pago (id, id_viaje, id_chofer, pago_base, pago_inicial, pago_final, total_acumulado, metodo_pago, periodo_pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    pago.id,
                    pago.id_viaje,
                    pago.id_chofer,
                    pago.pago_base,
                    pago.pago_inicial,
                    pago.pago_final,
                    pago.total_acumulado,
                    pago.metodo_pago,
                    pago.periodo_pago
                )
            )
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, pago):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            sql = """
                UPDATE pago 
                SET id_viaje = %s, id_chofer = %s, pago_base = %s, pago_inicial = %s, pago_final = %s, total_acumulado = %s, metodo_pago = %s, periodo_pago = %s
                WHERE id = %s
            """
            cursor.execute(
                sql,
                (
                    pago.id_viaje,
                    pago.id_chofer,
                    pago.pago_base,
                    pago.pago_inicial,
                    pago.pago_final,
                    pago.total_acumulado,
                    pago.metodo_pago,
                    pago.periodo_pago,
                    pago.id
                )
            )
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "DELETE FROM pago WHERE id = %s",
                (id,)
            )
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("SELECT id FROM pago ORDER BY id DESC")
            resultado = cursor.fetchone()
        finally:
            cursor.close()
            conexion.close()

        if resultado is None:
            return 0
        return resultado[0]