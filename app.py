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
                print("==================================================")
                print(
                    f"ID: {viaje.id}, Origen: {viaje.origen}, "
                    f"Destino: {viaje.destino}, Fecha: {viaje.fecha}, "
                    f"Hora: {viaje.hora}, Unidad ID: {viaje.id_unidad}, Chofer: {viaje.id_chofer}, "
                    f"Ruta: {viaje.id_ruta}, Estatus: {viaje.estatus}"
                )

    except Exception as e:
        print("Error al ver los viajes")
        print(e)

def insertar_viaje():
    try:
        origen = input("Origen: ")
        destino = input("Destino: ")
        fecha = input("Fecha (AAAA-MM-DD): ")
        hora = input("Hora (HH:MM:SS): ")
        id_unidad = int(input("ID de la unidad: "))
        estatus = input("Estatus: ")
        id_chofer = int(input("ID del chofer: "))
        id_ruta = int(input("ID de la ruta: "))

        viaje = Viaje(
            origen=origen,
            destino=destino,
            fecha=fecha,
            hora=hora,
            estatus=estatus,
            id_unidad=id_unidad,
            id_chofer=id_chofer,
            id_ruta=id_ruta
        )

        viaje_dao = ViajeDAO()
        viaje_dao.insertar(viaje)

        print("Viaje insertado correctamente.")

    except Exception as e:
        print("Error al insertar el viaje")
        print(e)

def actualizar_viaje():
    try:
  
        id_viaje = int(input("Ingrese el ID del viaje a actualizar: "))
        origen = input("Nuevo Origen: ")
        destino = input("Nuevo Destino: ")
        fecha = input("Nueva Fecha (AAAA-MM-DD): ")
        hora = input("Nueva Hora (HH:MM:SS): ")
        estatus = input("Nuevo Estatus: ")
        id_unidad = int(input("Nuevo ID de la unidad: "))
        id_chofer = int(input("Nuevo ID del chofer: "))
        id_ruta = int(input("Nuevo ID de la ruta: "))

        viaje = Viaje(
            id=id_viaje,
            origen=origen,
            destino=destino,
            fecha=fecha,
            hora=hora,
            estatus=estatus,
            id_unidad=id_unidad,
            id_chofer=id_chofer,
            id_ruta=id_ruta
        )

        viaje_dao = ViajeDAO()
        viaje_dao.actualizar(viaje)

        print("Viaje actualizado correctamente.")

    except Exception as e:
        print("Error al actualizar el viaje")
        print(e)

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
                    f"Tipo de licencia: {chofer.tipo_licencia}, Vigencia de licencia: {chofer.vigen_licencia}, "
                    f"Estatus: {chofer.estatus}"
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
        nombre = input("Escribe el nuevo nombre: ")
        telefono = input("Escribe el nuevo telefono: ")
        licencia = input("Escribe la nueva licencia: ")
        tipo_licencia = input("Escribe el nuevo tipo de licencia: ")
        vigen_licencia = input("Escribir la nueva vigencia de la licencia: ")
        estatus = input("Escribir el nuevo estatus del chofer: ")
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

#============================================================#
from dao.pagos_dao import PagoDAO
from models.pago import Pago

def ver_pagos():
    try:
        pago_dao = PagoDAO()

        pagos = pago_dao.obtener_todos()

        print("=== Lista de pagos ===")

        if len(pagos) == 0:
            print("No hay pagos registradas.")
        else:
            for pago in pagos: 
                print("====================================")
                print(
                    f"ID: {pago.id}, ID del viaje: {pago.id_viaje} "
                    f"Nombre del chofer: {pago.nombre_chofer}, Pago base: {pago.pago_base}, Pago inicial: {pago.pago_inicial}, "
                    f"Pago final: {pago.pago_final}, El pago total acumulado: {pago.total_acumulado}, "
                    f"Metodo del pago {pago.metodo_pago}, Periodo del pago: {pago.periodo_pago}"
                    
                )
                print("====================================")
        print("\n Conexión exitosa a la base de datos")
    except Exception as e:
        print("Error: ")
        print(e)
        
def insertar_pagos():
    id_chofer = input ("ID del chofer del cual se inserta el pago: ")
    id_viaje = input ("ID de los viajes del cual se le pagan: ")
    pago_base = input("Pago base: ")
    pago_inicial = input("Pago inicial: ")
    pago_final = input("Pago final: ")
    total_acumulado = input("Pago total acumulado: ")
    metodo_pago = input ("Metodo del pago: ")
    periodo_pago = input ("¿En que periodo se hace el pago?: ")
    try:
        pago_dao = PagoDAO()
        id = pago_dao.obtener_ultimo_id() + 1
        pago = Pago(
            id=id,
            id_viaje=id_viaje,
            id_chofer=id_chofer,
            pago_base=pago_base,
            pago_inicial=pago_inicial,
            pago_final=pago_final,
            total_acumulado=total_acumulado,
            metodo_pago=metodo_pago,
            periodo_pago=periodo_pago
        )
        pago_dao.insertar(pago)
        print("Inserción realizada con éxito")
    except Exception as e:
        print("Error al insertar un nuevo chofer")
        print(e)

def actualizar_pagos():
    print("Selecciona el pago a actualizar")
    pago_dao = PagoDAO()
    
    try:
        ver_pagos()  
        id = int(input("Escribe el ID del pago a actualizar: "))
        id_viaje = input("Escribe el nuevo ID del viaje: ")
        id_chofer = input("Escribe el nuevo ID del chofer: ")
        pago_base = input("Escribe el nuevo pago base: ")
        pago_inicial = input("Escribe el nuevo pago inicial: ")
        pago_final = input("Escribe el nuevo pago final: ")
        total_acumulado = input("Escribe el nuevo pago total acumulado: ")
        metodo_pago = input("Escribe el nuevo método de pago: ")
        periodo_pago = input("Escribe el nuevo período de pago: ")
        
        pago = Pago(
            id=id,
            id_viaje=id_viaje,
            id_chofer=id_chofer,
            pago_base=pago_base,
            pago_inicial=pago_inicial,
            pago_final=pago_final,
            total_acumulado=total_acumulado,
            metodo_pago=metodo_pago,
            periodo_pago=periodo_pago
        )
        
        pago_dao.actualizar(pago)
        print(f"El pago con ID {id} se ha actualizado exitosamente")

    except Exception as e:
        print("Error al actualizar un pago")
        print(e)
        
def eliminar_pagos():
    try:
        pago_dao = PagoDAO()
        print("Lista de pagos disponibles: ")
        ver_pagos()
        id = int(input("Escribe el id del pago a eliminar: "))
        pago_dao.eliminar(id)
        print(f"El pago {id} ha sido eliminado con éxito")
    except Exception as e:
        print(f"Error al eliminar el pago {id}")
        print(e)
        
def menu_pagos():
    print("1. Ver todos los pagos")
    print("2. Insertar un pago nuevo")
    print("3. Actualizar un pago")
    print("4. Eliminar un pago")
    opcion = int(input("Seleccionar una opcion (1-4): "))
    
    match opcion:
        case 1:
            ver_pagos()
        case 2:
            insertar_pagos()
        case 3:
            actualizar_pagos()
        case 4:
            eliminar_pagos()
            
            
            
            
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

usuario_actual = None

def ver_perfil():
    global usuario_actual
    
    if usuario_actual is None:
        print("\nNo has iniciado sesión.")
        return

    print("\n=== PERFIL DE USUARIO ===")
    print("====================================")
    print(f"ID: {usuario_actual.id}")
    print(f"Nombre: {usuario_actual.nombre}")
    print(f"Correo: {usuario_actual.correo}")
    print(f"Rol: {usuario_actual.rol}")
    print("====================================")


def registrar_usuario():
    nombre = input("Escribe tu nombre completo: ")
    correo = input("Escribe tu correo electronico: ")
    contrasena = input("Escribe tu contraseña: ")
    rol = "admin"
    try:
        usuario_dao = UsuarioDAO()
        id = usuario_dao.obtener_ultimo_id() + 1
        usuario = Usuario(
            id=id,
            nombre=nombre,
            correo=correo,
            contrasena=contrasena,
            rol=rol
        )
        usuario_dao.registrar(usuario)
        print("Registro realizado con éxito")
    except Exception as e:
        print("Error al registrar un nuevo usuario")
        print(e)

def iniciar_sesion():
    global usuario_actual
    correo = input("Correo electronico: ")
    contrasena = input("Contraseña: ")
    try:
        usuario_dao = UsuarioDAO()
        usuario = usuario_dao.login(correo, contrasena)
        
        if usuario is not None:
            usuario_actual = usuario  # Guardamos la sesión
            print(f"\nBienvenido {usuario.nombre}")
            return True
        else:
            print("Correo o contraseña incorrectos")
            return False
    except Exception as e:
        print("Error al iniciar sesion")
        print(e)
        return False

def menu_usuarios():
    print("1. Registrar usuario nuevo")
    print("2. Iniciar sesion")
    print("3. Ver perfil")
    
    opcion = int(input("Seleccionar una opcion (1-2): "))
    
    match opcion:
        case 2:
            iniciar_sesion()
            ver_perfil()
        case 1:
            registrar_usuario()
        case 3:
            ver_perfil()


def main():
    print("=== SISTEMA UNIRUTA ===")
    print("Menú de opciones")
    print("1. Usuarios")
    print("2. Unidades")
    print("3. Choferes")
    print("4. Rutas")
    print("5. Viajes")
    print("6. Pagos")

    opc = int(input("Selecciona una opcion: "))

    match opc:
        case 1:
            menu_usuarios()
        case 2:
            menu_unidades()
        case 3:
            menu_choferes()  
        case 4:
            menu_rutas() 
        case 5:
            menu_viajes()
        case 6: 
            menu_pagos()
 




if __name__ == "__main__":
    main()