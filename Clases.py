class Habitacion:
    def __init__(self, id_habitacion, tipo, vista_mar, piso):
        self.id = id_habitacion
        self.tipo = tipo
        self.vista_mar = vista_mar
        self.piso = piso


class Servicio:
    def __init__(self, nombre, capacidad_total):
        self.nombre = nombre
        self.capacidad_total = capacidad_total


class Reserva:
    def __init__(self, cliente, habitaciones_ids, servicios_nombres, check_in, check_out):
        self.cliente = cliente
        self.habitaciones_ids = habitaciones_ids
        self.servicios_nombres = servicios_nombres
        self.check_in = check_in       
        self.check_out = check_out        

    def to_dict(self):
        return {
            "cliente": self.cliente,
            "habitaciones": self.habitaciones_ids,
            "servicios": self.servicios_nombres,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat()
        }