from database.conexion import Conexion
from models.viaje import Viaje

class ViajeDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
            
        cursor.execute("SELECT * FROM viaje")
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
            )

            viajes.append(viaje)

        cursor.close()
        conexion.close()

        return viajes
    
    def insertar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO viaje (origen, destino, fecha, hora, id_unidad, estatus)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,(
            viaje.origen,
            viaje.destino,
            viaje.fecha,
            viaje.hora,
            viaje.id_unidad,
            viaje.estatus
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