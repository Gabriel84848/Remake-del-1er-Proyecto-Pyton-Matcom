from datetime import date, timedelta
from Clases import Reserva

def validar_check_in(check_in):
   
    hoy = date.today()
    max_fecha = hoy.replace(year=hoy.year + 2)
    
    if check_in < hoy:
        return False, f"El check-in no puede ser en el pasado (hoy es {hoy.strftime('%d-%m-%Y')})."
    if check_in > max_fecha:
        return False, f"No se aceptan reservas con más de 2 años de antelación (máximo {max_fecha.strftime('%d-%m-%Y')})."
    return True, "Check-in válido."

def validar_nombre(nombre):
    nombre_limpio = nombre.strip()
    
    if len(nombre_limpio) < 3:
        return False, "No aceptamos personas con menos de 3 letras en el nombre."

    for char in nombre_limpio:
        
        #isalpha para no tener que permitir 1 a 1 las letras
        if not (char.isalpha() or char in " -'’"):
            return False, "Imposible que tengas eso en tu nombre."
    
    return True, "Nombre válido."

def validar_check_out(check_in, check_out):
  
    if check_out <= check_in:
        return False, "El check-out debe ser después del check-in."
    if (check_out - check_in).days < 1:
        return False, "La estancia mínima es de 1 día."
    return True, "Check-out válido."

def validar_fechas(check_in, check_out):

    valido, msg = validar_check_in(check_in)
    if not valido:
        return False, msg
    valido, msg = validar_check_out(check_in, check_out)
    if not valido:
        return False, msg
    return True, "Fechas válidas."

def verificar_disponibilidad_habitacion(id_hab, check_in, check_out, reservas):
    
    for res in reservas:
        # Si la reserva incluye la habitacion
        if id_hab in res.habitaciones_ids:
            # Verificar que no se superpongan
            if check_in < res.check_out and check_out > res.check_in:
                return False
    return True

def verificar_disponibilidad_servicio(nombre_servicio, check_in, check_out, servicios, reservas):
    
    # Buscar el objeto servicio
    servicio_obj = None
    for s in servicios:
        if s.nombre == nombre_servicio:
            servicio_obj = s
            break
    if not servicio_obj:
        return 0

    # Contar cuantos servicios esta ocupados en el int
    ocupados = 0
    for res in reservas:
        if check_in < res.check_out and check_out > res.check_in:  # que no se superpongan
            for item in res.servicios_nombres:
                if item.startswith(nombre_servicio + ":"):
                    try:
                        ocupados += int(item.split(":")[1])
                    except:
                        pass

    disponibles = servicio_obj.capacidad_total - ocupados
    return disponibles

#Por si acaso aunque en la interfaz no hay forma de que ocura
def validar_exclusion_mutua(servicios_solicitados):
    PAREJAS_EXCLUIDAS = [("masaje", "yoga"),]
    
    # Extraemoa nombres de los serv
    nombres_servicios = [s.split(":")[0] for s in servicios_solicitados]
    
    # Verificamos si esta
    for servicio_a, servicio_b in PAREJAS_EXCLUIDAS:
        if servicio_a in nombres_servicios and servicio_b in nombres_servicios:
            return False, f"No se pueden reservar '{servicio_a}' y '{servicio_b}' en la misma estancia."
    
    return True, ""

def obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios):
    
    disponibles = []
    for hab in habitaciones:
        # Verificar ocupacion
        if not verificar_disponibilidad_habitacion(hab.id, check_in, check_out, reservas):
            continue

        # Si es suite, verificar que haya al menos 1 desayuno disponible
        if hab.id == "H204":
            desayunos_disp = verificar_disponibilidad_servicio("desayuno", check_in, check_out, servicios, reservas)
            if desayunos_disp < 1:
                continue  # no mostrar la suite si no hay desayunos

        disponibles.append(hab)
    return disponibles

def validar_restricciones_habitaciones(habitaciones_ids, habitaciones, reservas, check_in, check_out, servicios):
    
    if not habitaciones_ids:
        return False, "Debes seleccionar al menos una habitación.", []

    if len(habitaciones_ids) > 2:
        return False, "Máximo 2 habitaciones por reserva.", []

    # Verificar duplicados
    if len(set(habitaciones_ids)) != len(habitaciones_ids):
        return False, "No puedes seleccionar la misma habitación dos veces.", []

    # Verificar existencia y obtener objetos habitacion
    habitaciones_validas = []
    for id_hab in habitaciones_ids:
        hab_obj = None
        for h in habitaciones:
            if h.id == id_hab:
                hab_obj = h
                break
        if not hab_obj:
            return False, f"La habitación '{id_hab}' no existe.", []
        habitaciones_validas.append(hab_obj)

    # verificar disponibilidad (usar la misma logica de obtener_habitaciones_disponibles)
    disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios)
    ids_disponibles = [h.id for h in disponibles]
    for id_hab in habitaciones_ids:
        if id_hab not in ids_disponibles:
            # si la suite no tiene desayuno
            if id_hab == "H204":
                return False, "La suite H204 no está disponible porque no hay desayunos en esas fechas.", []
            return False, f"La habitación '{id_hab}' no está disponible en esas fechas.", []

    # Verificar mismo piso
    if len(habitaciones_validas) == 2:
        if habitaciones_validas[0].piso != habitaciones_validas[1].piso:
            return False, "Las habitaciones deben estar en el mismo piso.", []

    return True, "Habitaciones válidas.", habitaciones_validas

def crear_reserva_sistema(cliente, habitaciones_ids, servicios_solicitados,check_in, check_out, habitaciones, servicios, reservas):

    valido, mensaje = validar_exclusion_mutua(servicios_solicitados)
    if not valido:
        return False, mensaje, None

    nueva_reserva = Reserva(cliente, habitaciones_ids, servicios_solicitados, check_in, check_out)
    reservas.append(nueva_reserva)
    return True, "Reserva creada exitosamente.", nueva_reserva

def buscar_hueco_automatico(habitaciones_ids, servicios_solicitados, noches, habitaciones, servicios, reservas):
    
    valido, _ = validar_exclusion_mutua(servicios_solicitados)
    if not valido:
        return None, None

    hoy = date.today()
    limite = hoy.replace(year=hoy.year + 2)
    
    #Recorremos dede hoy hasta el lim
    fecha = hoy
    while fecha <= limite:
        check_in = fecha
        check_out = check_in + timedelta(days=noches)
        
        # Verificar disponibilidad de habitaciones
        disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios)
        ids_disponibles = [h.id for h in disponibles]
        
        todas_disponibles = all(id_hab in ids_disponibles for id_hab in habitaciones_ids)
        if not todas_disponibles:
            fecha += timedelta(days=1)
            continue
        
        #Verificar disponibilidad de servicios
        servicios_ok = True
        for servicio_str in servicios_solicitados:
            nombre, cant_str = servicio_str.split(":")
            cantidad = int(cant_str)
            if cantidad > 0:
                disponibles_servicio = verificar_disponibilidad_servicio(nombre, check_in, check_out, servicios, reservas)
                if cantidad > disponibles_servicio:
                    servicios_ok = False
                    break
        
        if servicios_ok:
            return check_in, check_out
        
        fecha += timedelta(days=1)
    
    return None, None