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
                tiempo_estimado=registro[4],
                # Columnas nuevas: se leen con protección por si la BD
                # todavía no tiene el ALTER TABLE aplicado
                observaciones=registro[5] if len(registro) > 5 else None,
                tarifa=registro[6] if len(registro) > 6 else None,
            )
            rutas.append(ruta)
        cursor.close()
        conexion.close()

        return rutas

    def buscar_por_nombre(self, filtro):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM ruta WHERE nombre ILIKE %s",
            (f"%{filtro}%",),
        )
        registros = cursor.fetchall()

        rutas = []
        for registro in registros:
            ruta = Ruta(
                id=registro[0],
                nombre=registro[1],
                origen=registro[2],
                destino=registro[3],
                tiempo_estimado=registro[4],
                observaciones=registro[5] if len(registro) > 5 else None,
                tarifa=registro[6] if len(registro) > 6 else None,
            )
            rutas.append(ruta)
        cursor.close()
        conexion.close()

        return rutas

    def insertar(self, ruta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO ruta (id, nombre, origen, destino, tiempo_estimado, observaciones, tarifa)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                ruta.id,
                ruta.nombre,
                ruta.origen,
                ruta.destino,
                ruta.tiempo_estimado,
                ruta.observaciones,
                ruta.tarifa,
            ),
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, ruta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE ruta
        SET nombre = %s, origen = %s, destino = %s, tiempo_estimado = %s,
            observaciones = %s, tarifa = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (
                ruta.nombre,
                ruta.origen,
                ruta.destino,
                ruta.tiempo_estimado,
                ruta.observaciones,
                ruta.tarifa,
                ruta.id,
            ),
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, ruta_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM ruta WHERE id = %s",
            (ruta_id,),
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