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

def menu_unidades():
    print("1. Ver todas las unidades")
    print("2. Insertar una unidad nueva")
    print("3. Actualizar una unidad disponible")
    print("4. Eliminar una unidad disponible")
    opcion = int(input("Seleccionar una opcion (1-4): "))

    match opcion:
        case 1:
            ver_unidades()
        case 2:
            insertar_unidad()
        case 3:
            actualizar_unidad()
        case 4:
            eliminar_unidad()


def menu_choferes():
    print("1. Ver todos los choferes")
    print("2. Insertar un chofer nuevo")
    print("3. Actualizar un chofer disponible")
    print("4. Eliminar un chofer disponible")
    opcion = int(input("Seleccionar una opcion (1-4): "))

    match opcion:
        case 1:
            ver_choferes()
        case 2:
            insertar_chofer()
        case 3:
            actualizar_chofer()
        case 4:
            eliminar_chofer()
 
         
#============================================================#
from dao.chofer_dao import ChoferDAO
from models.chofer import Chofer

def ver_choferes():
    try:
        Chofer_dao = ChoferDAO()

        Choferes = Chofer_dao.obtener_todos()

        print("=== Lista de choferes ===")

        if len(Choferes) == 0:
            print("No hay choferes registrados.")
        else:
            for chofer in Choferes: 
                print("====================================")
                print(
                    f"ID: {chofer.id}, Nombre: {chofer.nombre}, "
                    f"telefono: {chofer.telefono}, Licencia: {chofer.licencia}, "
                    f"Tipo de licencia: {chofer.tipo_licencia}, Vigencia de licencia: {chofer.vigen_licencia}"
                    f"estatus: {chofer.estatus}"
                )
                print("====================================")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)
        
def main():
    print("=== SISTEMA UNIRUTA ===")
    print("Menú de opciones")
    print  ("1. Unidades")
    print("2. Choferes")
    
    opc = int(input("Selecciona una opcion: "))

    match opc:
        case 1:
            menu_unidades()
        case 2:
            menu_choferes()    
 




if __name__ == "__main__":
    main()