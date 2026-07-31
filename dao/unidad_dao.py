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
    
    def insertar(self, unidad):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        sql ="""
        INSERT INTO unidad (noeconomico, placas, modelo, marca, año, kilometraje, estatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
            unidad.noeconomico,
            unidad.placas,
            unidad.modelo,
            unidad.marca,
            unidad.año,
            unidad.kilometraje,
            unidad.estatus
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    def actualizar(self, unidad):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        sql ="""
        UPDATE unidad
        SET noeconomico = %s, placas = %s, modelo = %s, marca = %s, año = %s, kilometraje = %s, estatus = %s
        WHERE id = %s
        """

        cursor.execute(
            sql,
            (unidad.noeconomico,
            unidad.placas,
            unidad.modelo,
            unidad.marca,
            unidad.año,
            unidad.kilometraje,
            unidad.estatus,
            unidad.id
            )
        )

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self, unidad_id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM unidad WHERE id = %s",
            (unidad_id,)
            )

        conexion.commit()
        cursor.close()
        conexion.close()