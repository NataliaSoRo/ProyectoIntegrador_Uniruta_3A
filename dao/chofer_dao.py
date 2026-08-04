import psycopg2

from database.conexion import Conexion
from models.chofer import Chofer

class ChoferDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM choferes")
        registros = cursor.fetchall()

        choferes = []
        for registro in registros:
            # Usamos argumentos con nombre para evitar desfasamientos
            chofer = Chofer(
                id=registro[0],
                nombre=registro[1],
                telefono=registro[2],
                licencia=registro[3],
                tipo_licencia=registro[4],
                vigen_licencia=registro[5],
                estatus=registro[6],  # La columna 6 en la BD es estatus
                foto=registro[7] if len(registro) > 7 else None,  # La columna 7 es la foto nueva
                observaciones=registro[8] if len(registro) > 8 else None  # La columna 8 es observaciones (nueva)
            )
            choferes.append(chofer)

        cursor.close()
        conexion.close()

        return choferes

    def buscar_por_nombre(self, filtro):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM choferes WHERE nombre LIKE %s",
            (f"%{filtro}%",)
        )
        registros = cursor.fetchall()

        choferes = []
        for registro in registros:
            chofer = Chofer(
                id=registro[0],
                nombre=registro[1],
                telefono=registro[2],
                licencia=registro[3],
                tipo_licencia=registro[4],
                vigen_licencia=registro[5],
                estatus=registro[6],
                foto=registro[7] if len(registro) > 7 else None,
                observaciones=registro[8] if len(registro) > 8 else None
            )
            choferes.append(chofer)

        cursor.close()
        conexion.close()

        return choferes

    def insertar(self, chofer):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        # Función para leer campos sea diccionario u objeto
        def obtener(obj, clave, defecto=None):
            if isinstance(obj, dict):
                return obj.get(clave, defecto)
            return getattr(obj, clave, defecto)

        sql = """
        INSERT INTO choferes (nombre, telefono, licencia, tipo_licencia, vigen_licencia, foto, estatus, observaciones)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                obtener(chofer, "nombre"),
                obtener(chofer, "telefono"),
                obtener(chofer, "licencia"),
                obtener(chofer, "tipo_licencia"),
                obtener(chofer, "vigen_licencia"),
                obtener(chofer, "foto"),  # Lee la ruta o nombre de la foto
                obtener(chofer, "estatus", "Activo"),
                obtener(chofer, "observaciones"),  # Lee las observaciones (nuevo)
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, chofer):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        # Mismo helper que insertar(), para soportar dict u objeto
        def obtener(obj, clave, defecto=None):
            if isinstance(obj, dict):
                return obj.get(clave, defecto)
            return getattr(obj, clave, defecto)

        sql = """
        UPDATE choferes
        SET nombre = %s, telefono = %s, licencia = %s, tipo_licencia = %s,
            vigen_licencia = %s, foto = %s, estatus = %s, observaciones = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (
                obtener(chofer, "nombre"),
                obtener(chofer, "telefono"),
                obtener(chofer, "licencia"),
                obtener(chofer, "tipo_licencia"),
                obtener(chofer, "vigen_licencia"),
                obtener(chofer, "foto"),
                obtener(chofer, "estatus", "Activo"),
                obtener(chofer, "observaciones"),  # Nuevo
                obtener(chofer, "id"),
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, chofer_id):
        """
        Elimina un chofer de forma definitiva.
        Si el chofer tiene pagos asociados (fk_pago_chofer), la BD rechaza
        el borrado con ForeignKeyViolation. En ese caso, capturamos el error
        y lanzamos un ValueError con un mensaje claro para mostrar en la UI,
        en vez de dejar que el traceback crudo de psycopg2 llegue a la vista.
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "DELETE FROM choferes WHERE id = %s",
                (chofer_id,)
            )
            conexion.commit()
        except psycopg2.errors.ForeignKeyViolation:
            conexion.rollback()
            raise ValueError(
                "No se puede eliminar este chofer porque tiene pagos registrados. "
                "Cámbialo a estatus 'Inactivo' en vez de eliminarlo."
            )
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def desactivar(self, chofer_id):
        """
        Borrado lógico: en vez de eliminar el registro (lo cual falla si
        el chofer tiene pagos asociados), lo marca como 'Inactivo'.
        Recomendado como acción principal del botón de eliminar en la UI.
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "UPDATE choferes SET estatus = %s WHERE id = %s",
            ("Inactivo", chofer_id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM choferes ORDER BY id DESC")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]