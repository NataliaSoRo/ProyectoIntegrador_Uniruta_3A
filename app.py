from dao.unidad_dao import UnidadDAO
from models.unidad import Unidad
from dao.viaje_dao import ViajeDAO
from models.viaje import Viaje

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

def insertar_unidad():
    try:
        noeconomico = input("Número económico: ")
        placas = input("Placas: ")
        modelo = input("Modelo: ")
        marca = input("Marca: ")
        año = int(input("Año: "))
        kilometraje = int(input("Kilometraje: "))
        estatus = input("Estatus: ")

        unidad = Unidad(
            id=None,
            noeconomico=noeconomico,
            placas=placas,
            modelo=modelo,
            marca=marca,
            año=año,
            kilometraje=kilometraje,
            estatus=estatus
        )

        unidad_dao = UnidadDAO()
        unidad_dao.insertar(unidad)

        print("Unidad insertada correctamente.")

    except Exception as e:
        print("Error al insertar la unidad")
        print(e)

def actualizar_unidad():
    try:
        id = int(input("ID de la unidad: "))
        noeconomico = input("Nuevo número económico: ")
        placas = input("Nuevas placas: ")
        modelo = input("Nuevo modelo: ")
        marca = input("Nueva marca: ")
        año = int(input("Nuevo año: "))
        kilometraje = int(input("Nuevo kilometraje: "))
        estatus = input("Nuevo estatus: ")

        unidad = Unidad(
            id=id,
            noeconomico=noeconomico,
            placas=placas,
            modelo=modelo,
            marca=marca,
            año=año,
            kilometraje=kilometraje,
            estatus=estatus
        )

        unidad_dao = UnidadDAO()
        unidad_dao.actualizar(unidad)

        print("Unidad actualizada correctamente.")

    except Exception as e:
        print("Error al actualizar la unidad")
        print(e)

def eliminar_unidad():
    try:
        id = int(input("ID de la unidad a eliminar: "))

        unidad_dao = UnidadDAO()
        unidad_dao.eliminar(id)

        print("Unidad eliminada correctamente.")

    except Exception as e:
        print("Error al eliminar la unidad")
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

from dao.viaje_dao import ViajeDAO
from models.viaje import Viaje

def ver_viajes():
    try:
        viaje_dao = ViajeDAO()
        viajes = viaje_dao.obtener_todos()

        print("=== Viajes registrados ===")

        if len(viajes) == 0:
            print("No hay viajes registrados.")
        else:
            for viaje in viajes:
                print("====================================")
                print(
                    f"ID: {viaje.id}, Origen: {viaje.origen}, "
                    f"Destino: {viaje.destino}, Fecha: {viaje.fecha}, "
                    f"Hora: {viaje.hora}, Unidad ID: {viaje.unidad}, "
                    f"Estatus: {viaje.estatus}"
                )

    except Exception as e:
        print("Error al ver los viajes")
        print(e)

def insertar_viaje():
    print("Insertar viaje")

    origen = input("Origen: ")
    destino = input("Destino: ")
    fecha = input("Fecha (AAAA-MM-DD): ")
    hora = input("Hora (HH:MM:SS): ")
    unidad = int(input("ID de la unidad: "))
    estatus = input("Estatus: ")

    viaje = Viaje(
        origen=origen,
        destino=destino,
        fecha=fecha,
        hora=hora,
        unidad=unidad,
        estatus=estatus
    )

    viaje_dao = ViajeDAO()
    viaje_dao.insertar_viaje(viaje)

    print("Viaje registrado correctamente.")

def actualizar_viaje():
      print("selecciona el viaje a actualizar")

      id = int(input("ID del viaje a actualizar: "))
      origen = input("Nuevo origen: ")
      destino = input("Nuevo destino: ")
      fecha = input("Nueva fecha (AAAA-MM-DD): ")
      hora = input("Nueva hora (HH:MM:SS): ")
      unidad = int(input("Nuevo ID de la unidad: "))
      estatus = input("Nuevo estatus: ")
      
      viaje = Viaje(
        id=id,
        origen=origen,
        destino=destino,
        fecha=fecha,
        hora=hora,
        unidad=unidad,
        estatus=estatus
      )
    
      viaje_dao = ViajeDAO()
      viaje_dao.actualizar(viaje)
    
      print("Viaje actualizado correctamente.")

    
def eliminar_viaje():
    try:
        id = int(input("ID del viaje a eliminar: "))

        viaje_dao = ViajeDAO()
        viaje_dao.eliminar(id)

        print("Viaje eliminado correctamente.")

    except Exception as e:
        print("Error al eliminar el viaje")
        print(e)

def menu_viajes():
    print("=== Menú de viajes ===")
    print("1. Ver viajes")
    print("2. Insertar viaje")
    print("3. Actualizar viaje")
    print("4. Eliminar viaje")

    opcion = int(input("Seleccionar una opcion (1-4): "))

    match opcion:
        case 1:
            ver_viajes()
        case 2:
            insertar_viaje()
        case 3:
            actualizar_viaje()
        case 4:
            eliminar_viaje()



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
 
def menu_rutas():
    print("1. Ver todas las rutas")
    print("2. Insertar una ruta nueva")
    print("3. Actualizar una ruta disponible")
    print("4. Eliminar una ruta disponible")
    opcion = int(input("Seleccionar una opcion (1-4): "))

    match opcion:
        case 1:
            ver_rutas()
        case 2:
            insertar_rutas()
        case 3:
            actualizar_rutas()
        case 4:
            eliminar_rutas()
         
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

#============================================================#
from dao.ruta_dao import RutaDAO
from models.ruta import Ruta

def ver_rutas():
    try:
        ruta_dao = RutaDAO()

        rutas = ruta_dao.obtener_todos()

        print("=== Lista de rutas ===")

        if len(rutas) == 0:
            print("No hay rutas registradas.")
        else:
            for ruta in rutas: 
                print("====================================")
                print(
                    f"ID: {ruta.id}, Nombre: {ruta.nombre}, "
                    f"Origen: {ruta.origen}, Destino: {ruta.destino}, "
                    f"Tiempo estimado: {ruta.tiempo_estimado}"
                )
                print("====================================")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)
        
def insertar_rutas():
    nombre = input("Escribe el nombre de la ruta nueva: ")
    origen = input("Escribe el origen de la ruta nueva: ")
    destino = input("Escribe el destino de la ruta nueva: ")
    tiempo_estimado = input("Escribe el tiempo estimado de la ruta nueva: ")
    try:
        ruta_dao = RutaDAO()
        id_ruta = ruta_dao.obtener_ultimo_id() + 1
        ruta = Ruta(id_ruta, nombre, origen, destino, tiempo_estimado)
        ruta_dao.insertar(ruta)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo chofer")
        print(e)

def actualizar_rutas():
    print("Selecciona al usuario a actualizar")
    try:
        ruta_dao = RutaDAO()
        ver_rutas()
        id = int(input("Escribe el id de la ruta a actualizar: "))
        nombre = input("Escribe el nuevo nombre: ")
        origen = input("Escribe el nuevo origen: ")
        destino = input("Escribe el nuevo destino: ")
        tiempo_estimado = input("Escribe el nuevo tiempo estimado: ")
        ruta = Ruta (id, nombre, origen, destino, tiempo_estimado)
        ruta_dao.actualizar(ruta)
        print(f"La ruta {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar una ruta")
        print(e)
        
def eliminar_rutas():
    try:
        ruta_dao = RutaDAO()
        print("Lista de rutas disponibles: ")
        ver_rutas()
        id = int(input("Escribe el id de la ruta a eliminar: "))
        ruta_dao.eliminar(id)
        print(f"La ruta {id} ha sido eliminado con éxito")
    except Exception as e:
        print(f"Error al eliminar la ruta {id}")
        print(e)


def main():
    print("=== SISTEMA UNIRUTA ===")
    print("Menú de opciones")
    print("1. Unidades")
    print("2. Choferes")
    print("3. Rutas")
    print("4. Viajes")

    opc = int(input("Selecciona una opcion: "))

    match opc:
        case 1:
            menu_unidades()
        case 2:
            menu_choferes()  
        case 3:
            menu_rutas() 
        case 4:
            menu_viajes()
 




if __name__ == "__main__":
    main()