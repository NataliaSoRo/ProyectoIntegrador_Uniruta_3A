class Usuario:
    def __init__(self, id=None, nombre=None, correo=None, contrasena=None, rol="usuario"):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol