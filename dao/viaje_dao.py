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
                viaj_id=registro[0],
                viaj_origen=registro[1],
                viaj_destino=registro[2],
                viaj_fecha=registro[3],
                viaj_hora=registro[4],
                viaj_unid_id=registro[5],
                viaj_estatus=registro[6]
            )

            viajes.append(viaje)

        cursor.close()
        conexion.close()

        return viajes
    
def insertar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO viaje (viaj_origen, viaj_destino, viaj_fecha, viaj_hora, viaj_unid_id, viaj_estatus)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,(
            viaje.viaj_origen,
            viaje.viaj_destino,
            viaje.viaj_fecha,
            viaje.viaj_hora,
            viaje.viaj_unid_id,
            viaje.viaj_estatus
            ))

        conexion.commit()
        cursor.close()
        conexion.close()

def actualizar(self, viaje):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE viaje
        SET viaj_origen = %s, viaj_destino = %s, viaj_fecha = %s, viaj_hora = %s, viaj_unid_id = %s, viaj_estatus = %s
        WHERE viaj_id = %s
        """, (
            viaje.viaj_origen,
            viaje.viaj_destino,
            viaje.viaj_fecha,
            viaje.viaj_hora,
            viaje.viaj_unid_id,
            viaje.viaj_estatus,
            viaje.viaj_id
            ))

        conexion.commit()
        cursor.close()
        conexion.close()

def eliminar(self, viaje_id):
    conexion = Conexion.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM viaje WHERE viaj_id = %s", 
        (viaje_id,)
    )

    conexion.commit()
    cursor.close()
    conexion.close()