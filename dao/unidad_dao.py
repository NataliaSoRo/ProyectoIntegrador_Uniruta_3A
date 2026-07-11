from database.conexion import Conexion
from models.unidad import Unidad

class UnidadDAO:

    def obtener_todos(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
            
        cursor.execute("SELECT * FROM unidad")
        registros = cursor.fetchall()

        unidades = []
        for registro in registros:

            unidad = Unidad(
                id=registro[0],
                noeconomico=registro[1],
                placas=registro[2],
                modelo=registro[3],
                marca=registro[4],
                año=registro[5],          
                kilometraje=registro[6],
                estatus=registro[7])
            unidades.append(unidad)
        cursor.close()
        conexion.close()

        return unidades