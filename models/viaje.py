class Viaje:

    def __init__(
        self,
        id=None,
        origen=None,
        destino=None,
        fecha=None,
        hora=None,
        hora_llegada=None,
        pasajeros=None,
        observaciones=None,
        id_unidad=None,
        estatus=None,
        id_chofer=None,
        id_ruta=None,
        chofer_nombre=None,
        ruta_nombre=None,
    ):

        self.id = id
        self.origen = origen
        self.destino = destino
        self.fecha = fecha
        self.hora = hora
        self.hora_llegada = hora_llegada
        self.pasajeros = pasajeros
        self.observaciones = observaciones
        self.id_unidad = id_unidad
        self.estatus = estatus
        self.id_chofer = id_chofer
        self.id_ruta = id_ruta
        self.chofer_nombre = chofer_nombre
        self.ruta_nombre = ruta_nombre