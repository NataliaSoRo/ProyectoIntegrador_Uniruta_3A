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
    
    def insertar(self, ruta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql ="""
        INSERT INTO ruta (id, nombre, origen, destino, tiempo_estimado)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (ruta.id,
            ruta.nombre,
            ruta.origen,
            ruta.destino,
            ruta.tiempo_estimado
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM ruta ORDER BY id DESC")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]