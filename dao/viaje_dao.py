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
                unidad=registro[6],
               
            )

            viajes.append(viaje)

        cursor.close()
        conexion.close()

        return viajes
    
    def insertar_viaje(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO viaje (origen, destino, fecha, hora, estatus, unidad)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (viaje.origen,
            viaje.destino,
            viaje.fecha,
            viaje.hora,
            viaje.estatus,
            viaje.unidad,

            )
        )   
            

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE viaje
        SET origen = %s, destino = %s, fecha = %s, hora = %s, estatus = %s, unidad = %s
        WHERE id = %s
        """, (
            viaje.origen,
            viaje.destino,
            viaje.fecha,
            viaje.hora,
            viaje.estatus,
            viaje.unidad,
            viaje.id
            ))

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, viaje_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM viaje WHERE id = %s", 
            (viaje_id,)
        )

        conexion.commit()
        cursor.close()
        conexion.close()