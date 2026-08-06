import bcrypt
from database.conexion import Conexion
from models.usuario import Usuario


class UsuarioDAO:
    def registrar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            contrasena_hash = bcrypt.hashpw(
                usuario.contrasena.encode(), bcrypt.gensalt()
            ).decode()

            sql = """
                INSERT INTO usuario (nombre, correo, contrasena, rol)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql, (usuario.nombre, usuario.correo, contrasena_hash, usuario.rol)
            )
            conexion.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conexion.close()

    def login(self, correo, contrasena):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = "SELECT id, nombre, correo, contrasena, rol FROM usuario WHERE correo = %s"
            cursor.execute(sql, (correo,))
            registro = cursor.fetchone()

            if registro is None:
                return None

            hash_guardado = registro[3]
            if bcrypt.checkpw(contrasena.encode(), hash_guardado.encode()):
                return Usuario(
                    id=registro[0],
                    nombre=registro[1],
                    correo=registro[2],
                    rol=registro[4],
                )
            return None
        finally:
            cursor.close()
            conexion.close()

    def correo_existe(self, correo):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT 1 FROM usuario WHERE correo = %s", (correo,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conexion.close()