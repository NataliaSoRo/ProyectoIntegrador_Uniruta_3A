import psycopg2

from database.conexion import Conexion
from models.chofer import Chofer

class ChoferDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("SELECT * FROM choferes")
            registros = cursor.fetchall()
        except Exception as ex:
            print(f"[ChoferDAO] Error en obtener_todos: {ex}")
            registros = []
        finally:
            cursor.close()
            conexion.close()

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

        return choferes

    def buscar_por_nombre(self, filtro):
        """
        Busca choferes cuyo nombre, telefono, licencia, tipo de licencia o
        estatus coincidan (parcialmente) con el filtro ingresado.
        Usa ILIKE en vez de LIKE para que la busqueda no distinga entre
        mayusculas y minusculas (ej. "carlos" encuentra "Carlos Mendoza").

        telefono se castea a ::text porque en la base de datos esa columna
        es de tipo numerico (bigint), y el operador ILIKE solo funciona
        sobre texto.

        Si ocurre cualquier error (de conexion, de tipos de columna, etc.)
        se captura, se imprime en consola y se devuelve una lista vacia en
        vez de None, para que la vista nunca reciba algo no iterable.
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        patron = f"%{filtro}%"
        registros = []

        try:
            cursor.execute(
                """
                SELECT * FROM choferes
                WHERE nombre ILIKE %s
                   OR telefono::text ILIKE %s
                   OR licencia ILIKE %s
                   OR tipo_licencia ILIKE %s
                   OR estatus ILIKE %s
                """,
                (patron, patron, patron, patron, patron)
            )
            registros = cursor.fetchall()
        except Exception as ex:
            print(f"[ChoferDAO] Error en buscar_por_nombre: {ex}")
            try:
                conexion.rollback()
            except Exception:
                pass
            registros = []
        finally:
            cursor.close()
            conexion.close()

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
        Elimina un chofer de forma definitiva, junto con sus pagos asociados
        (borrado en cascada manual, ya que la FK en la BD no tiene ON DELETE
        CASCADE configurado).

        La tabla "pago" referencia al chofer mediante la columna "id_chofer".

        Ambos DELETE se ejecutan dentro de la misma transacción: si algo
        falla a mitad de camino, se hace rollback completo y no queda nada
        a medias (ni el chofer ni los pagos se eliminan).
        """
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        try:
            # 1) Borra primero los pagos asociados a este chofer
            cursor.execute(
                "DELETE FROM pago WHERE id_chofer = %s",
                (chofer_id,)
            )

            # 2) Ahora sí borra al chofer, ya sin pagos que lo bloqueen
            cursor.execute(
                "DELETE FROM choferes WHERE id = %s",
                (chofer_id,)
            )

            conexion.commit()
        except psycopg2.errors.ForeignKeyViolation:
            # Puede seguir ocurriendo si existe OTRA tabla con FK hacia
            # choferes que no sea "pago" (ej. viajes, unidades asignadas).
            conexion.rollback()
            raise ValueError(
                "No se puede eliminar este chofer porque tiene registros "
                "relacionados en otras tablas. Cámbialo a estatus 'Inactivo' "
                "en vez de eliminarlo."
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