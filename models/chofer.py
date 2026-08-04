class Chofer:
    def __init__(self, id=None, nombre=None, telefono=None, licencia=None,
                 tipo_licencia=None, vigen_licencia=None, foto=None,
                 estatus=None, observaciones=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.licencia = licencia
        self.tipo_licencia = tipo_licencia
        self.vigen_licencia = vigen_licencia
        self.foto = foto
        self.estatus = estatus
        self.observaciones = observaciones  # <-- Nuevo campo