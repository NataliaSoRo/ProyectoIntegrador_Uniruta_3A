from dao.unidad_dao import UnidadDAO
from models.unidad import Unidad

def ver_unidades():
     try:
          unidad_dao = UnidadDAO()
          unidades = unidad_dao.obtener_todos()

          print("=== Unidades en la base de datos ===")

          if len(unidades) == 0:
                 print("No hay unidades registradas.")

          else:
            print("Lista de unidades disponibles:")
          for unidad in unidades:
              print("----------------------------------------------")
              print(
                  f"ID: {unidad.id}, No. Economico: {unidad.noeconomico},"
                  f"Placas: {unidad.placas}, Modelo: {unidad.modelo},"
                  f"Marca: {unidad.marca}, Año: {unidad.año},"
                  f"Kilometraje: {unidad.kilometraje}, Estatus: {unidad.estatus}"
              )
              print("----------------------------------------------")
     except Exception as e:
          print("Error al ver las unidades")
          print(e)

def main():
    print("=== UNIDADES ===")
    print("Menu de opciones")
    print("1, Ver todas las unidades disponibles")
    print("2, Insertar una nueva unidad")
    print("3, Actualizar una unidad disponible")
    print("4, Eliminar una unidad disponible")
    opcion = int(input("selecciona una opcion (1-4): "))

    match opcion:
         case 1:
              ver_unidades()
         case 2:
              insertar_unidad()
         case 3:
              actualizar_unidad()
         case 4:
              eliminar_unidad()     
         




if __name__ == "__main__":
    main()