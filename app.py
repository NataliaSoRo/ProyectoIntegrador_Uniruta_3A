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
        
def insertar_chofer():
    nombre = input("Escribe el nombre del nuevo chofer: ")
    telefono = int(input("Escribe el telefono del nuevo chofer: "))
    licencia = input("Escribe la licencia del nuevo chofer: ")
    tipo_licencia = input("Escribe el tipo de licencia del nuevo chofer: ")
    vigen_licencia = input("Escribe la vigencia de la licencia (AAAA-MM-DD): ")
    estatus = input("Escribe el estatus del nuevo chofer: ")
    try:
        chofer_dao = ChoferDAO()
        id_chofer = chofer_dao.obtener_ultimo_id() + 1
        chofer = Chofer(id_chofer, nombre, telefono, licencia, tipo_licencia, vigen_licencia, estatus)
        chofer_dao.insertar(chofer)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo chofer")
        print(e)

def actualizar_chofer():
    print("Selecciona al usuario a actualizar")
    try:
        chofer_dao = ChoferDAO()
        ver_choferes()
        id = int(input("Escribe el id del chofer a actualizar: "))
        nombre = input("Escribe el nuevo nombre")
        telefono = input("Escribe el nuevo telefono")
        licencia = input("Escribe la nueva licencia")
        tipo_licencia = input("Escribe el nuevo tipo de licencia")
        vigen_licencia = input("Escribir la nueva vigencia de la licencia: ")
        estatus = input("Escribir el nuevo estatus del chofer")
        chofer = Chofer(id, nombre, telefono, licencia, tipo_licencia, vigen_licencia, estatus)
        chofer_dao.actualizar(chofer)
        print(f"El usuario {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar un usuario")
        print(e)
        
def eliminar_chofer():
    try:
        chofer_dao = ChoferDAO()
        print("Lista de choferes disponibles: ")
        ver_choferes()
        id = int(input("Escribe el id del chofer a eliminar: "))
        chofer_dao.eliminar(id)
        print(f"El chofer {id} ha sido eliminado con éxito")
    except Exception as e:
        print(f"Error al eliminar el chofer {id}")
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