from database.conexion import Conexion
from models.usuario import Usuario

class UsuarioDAO:
    def registrar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        sql = """
            INSERT INTO usuario (nombre, correo, contrasena, rol)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (usuario.nombre, usuario.correo, usuario.contrasena, usuario.rol))
        
        conexion.commit()
        cursor.close()
        conexion.close()

    def login(self, correo, contrasena):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        
        sql = """
        SELECT id, nombre, correo, contrasena, rol FROM usuario WHERE correo = %s AND contrasena = %s
        """
        cursor.execute(sql, (correo, contrasena))
        registro = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if registro:
            return Usuario(id=registro[0], nombre=registro[1], correo=registro[2], rol=registro[4])
        return None
    
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM usuario ORDER BY id DESC")
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()

        if resultado is None:
            return 0
        return resultado[0]