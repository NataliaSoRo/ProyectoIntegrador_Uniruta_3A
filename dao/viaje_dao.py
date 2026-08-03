from database.conexion import Conexion
from models.viaje import Viaje

class ViajeDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                v.id, 
                v.origen, 
                v.destino, 
                v.fecha, 
                v.hora, 
                v.estatus, 
                v.id_unidad, 
                v.id_chofer,
                v.id_ruta,
                c.nombre AS chofer_nombre, 
                r.nombre AS ruta_nombre
            FROM viaje v
            LEFT JOIN choferes c ON v.id_chofer = c.id
            LEFT JOIN ruta r ON v.id_ruta = r.id
        """

        cursor.execute(sql)
        registros = cursor.fetchall()

        viajes = []

        for registro in registros:

            viaje = Viaje(
                id=registro[0],
                origen=registro[1],
                destino=registro[2],
                fecha=registro[3],
                hora=registro[4],
                estatus=registro[5],
                id_unidad=registro[6],
                id_chofer=registro[7],
                id_ruta=registro[8],
                chofer_nombre=registro[9],
                ruta_nombre=registro[10],
            )
            viajes.append(viaje)

        cursor.close()
        conexion.close()

        return viajes
    def insertar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO viaje (origen, destino, fecha, hora, estatus, id_unidad, id_chofer, id_ruta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,
           (
            viaje.origen,
            viaje.destino,
            viaje.fecha,
            viaje.hora,
            viaje.estatus,
            viaje.id_unidad,
            viaje.id_chofer,
            viaje.id_ruta
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE viaje
        SET origen = %s, destino = %s, fecha = %s, hora = %s, id_unidad = %s, estatus = %s
        WHERE id = %s
        """, (
            viaje.origen,
            viaje.destino,
            viaje.fecha,
            viaje.hora,
            viaje.id_unidad,
            viaje.estatus,
            viaje.id
            ))

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
        "DELETE FROM viaje WHERE id = %s", 
        (id,)
    )

        conexion.commit()
        cursor.close()
        conexion.close()