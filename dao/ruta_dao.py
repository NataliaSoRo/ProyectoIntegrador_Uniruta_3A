from database.conexion import Conexion
from models.ruta import Ruta

class RutaDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
            
        cursor.execute("SELECT * FROM ruta")
        registros = cursor.fetchall()

        rutas = []
        for registro in registros:

            ruta = Ruta(
                id=registro[0],
                nombre=registro[1],
                origen=registro[2],
                destino=registro[3],
                tiempo_estimado=registro[4]
                )
            rutas.append(ruta)
        cursor.close()
        conexion.close()

        return rutas