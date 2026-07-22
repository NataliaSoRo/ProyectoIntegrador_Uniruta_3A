class Pago:
    def __init__(self, id_pagos=None, id_viaje=None, id_chofer=None, pago_inicial=None, pago_final=None, pago_total_acumulado=None,  metodo_pago=None, periodo_pago=None):
        self.id_pagos=id_pagos
        self.id_viaje = id_viaje
        self.id_chofer = id_chofer
        self.pago_inicial = pago_inicial
        self.pago_final = pago_final
        self.pago_total_acumulado = pago_total_acumulado
        self.metodo_pago = metodo_pago
        self.periodo_pago = periodo_pago