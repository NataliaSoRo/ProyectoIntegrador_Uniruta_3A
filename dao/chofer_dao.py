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

            chofer = Chofer(
                id=registro[0],
                nombre=registro[1],
                telefono=registro[2],
                licencia=registro[3],
                tipo_licencia=registro[4],
                vigen_licencia=registro[5],          
                estatus=registro[6])
            choferes.append(chofer)
        cursor.close()
        conexion.close()

        return choferes
    
    def insertar(self, chofer):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql ="""
        INSERT INTO choferes (id, nombre, telefono, licencia, tipo_licencia, vigen_licencia, estatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (chofer.id,
            chofer.nombre,
            chofer.telefono,
            chofer.licencia,
            chofer.tipo_licencia,
            chofer.vigen_licencia,
            chofer.estatus)
        )

        conexion.commit()
        cursor.close()
        conexion.close()
        
    def actualizar(self, chofer):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql ="""
        UPDATE choferes
        SET nombre = %s, telefono = %s, licencia = %s, tipo_licencia = %s, vigen_licencia = %s, estatus = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (chofer.nombre,
            chofer.telefono,
            chofer.licencia,
            chofer.tipo_licencia,
            chofer.vigen_licencia,
            chofer.estatus,
            chofer.id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        
    def eliminar(self, chofer_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM choferes WHERE id = %s",
            (chofer_id,)
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
    
