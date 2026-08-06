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
                v.pasajeros,
                v.hora_llegada,
                v.observaciones,
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
                pasajeros=registro[9],
                hora_llegada=registro[10],
                observaciones=registro[11],
                chofer_nombre=registro[12],
                ruta_nombre=registro[13],
            )
            viajes.append(viaje)

        cursor.close()
        conexion.close()

        return viajes
    def insertar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        print("DAO origen:", viaje.origen)
        print("DAO destino:", viaje.destino)

        cursor.execute("""
        INSERT INTO viaje (
            origen,
            destino,
            fecha,
            hora,
            estatus,
            id_unidad,
            id_chofer,
            id_ruta,
            pasajeros,
            hora_llegada,
            observaciones
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            viaje.origen,
            viaje.destino,
            viaje.fecha,
            viaje.hora,
            viaje.estatus,
            viaje.id_unidad,
            viaje.id_chofer,
            viaje.id_ruta,
            viaje.pasajeros,
            viaje.hora_llegada,
            viaje.observaciones
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE viaje
        SET
            fecha = %s,
            hora = %s,
            hora_llegada = %s,
            pasajeros = %s,
            observaciones = %s,
            id_unidad = %s,
            id_chofer = %s,
            id_ruta = %s,
            estatus = %s
        WHERE id = %s
        """, (
            viaje.fecha,
            viaje.hora,
            viaje.hora_llegada,
            viaje.pasajeros,
            viaje.observaciones,
            viaje.id_unidad,
            viaje.id_chofer,
            viaje.id_ruta,
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