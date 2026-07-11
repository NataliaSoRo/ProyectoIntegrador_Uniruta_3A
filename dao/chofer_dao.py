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