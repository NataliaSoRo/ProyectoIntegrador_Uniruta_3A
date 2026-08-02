class Pago:
    def __init__(self, id=None, id_viaje=None, id_chofer=None, pago_base=None, pago_inicial=None, pago_final=None, total_acumulado=None,  metodo_pago=None, periodo_pago=None, nombre_chofer=None):
        self.id=id
        self.id_viaje= id_viaje
        self.id_chofer = id_chofer
        self.pago_base = pago_base
        self.pago_inicial = pago_inicial
        self.pago_final = pago_final
        self.total_acumulado = total_acumulado
        self.metodo_pago = metodo_pago
        self.periodo_pago = periodo_pago
        self.nombre_chofer = nombre_chofer