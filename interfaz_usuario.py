import os
from datetime import date
from guardar_y_cargar import guardar_datos
from logica_reservas import validar_check_in, validar_check_out
from logica_reservas import (
    obtener_habitaciones_disponibles,
    validar_restricciones_habitaciones,
    verificar_disponibilidad_servicio,
    crear_reserva_sistema,
    buscar_hueco_automatico,
    validar_nombre 
)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausa(mensaje="Presiona Enter para continuar..."):
    input(mensaje)

def ver_habitaciones_interfaz(reservas):
    
    ids_validos = ["H101", "H102", "H103", "H104", "H201", "H202", "H203", "H204"]
    while True:
        limpiar_pantalla()
        print("╔═══════════════════════════════════════════════╗")
        print("║           Catalogo de Habitaciones            ║")
        print("╠═══════════════════════════════════════════════╣")
        print("║  PISO 1:                                      ║")
        print("║  1: H101 (simple) - Piso 1 - Sin vista al mar ║")
        print("║  2: H102 (simple) - Piso 1 - Sin vista al mar ║")
        print("║  3: H103 (simple) - Piso 1 - Sin vista al mar ║")
        print("║  4: H104 (doble) - Piso 1 - Sin vista al mar  ║")
        print("╠═══════════════════════════════════════════════╣")
        print("║  PISO 2:                                      ║")
        print("║  1: H201 (simple) - Piso 2 - Vista al mar     ║")
        print("║  2: H202 (simple) - Piso 2 - Sin vista al mar ║")
        print("║  3: H203 (doble) - Piso 2 - Vista al mar      ║")
        print("║  4: H204 (suite) - Piso 2 - Vista al mar      ║")
        print("╚═══════════════════════════════════════════════╝")
        print()
        print("Para ver las reservas de una habitacion, escribe su ID (ej: H101)")
        print("Presiona Enter sin escribir para volver al menu principal")
        
        seleccion = input(">> ").strip().upper()
        if seleccion == "":
            return
        
        #Verificar que existe
        if seleccion not in ids_validos:
            limpiar_pantalla()
            print("=" * 50)
            print(f"     La habitación '{seleccion}' no existe.")
            print("=" * 50)
            pausa()
            continue
        
        # Reservas de esa hab
        reservas_habitacion = []
        for reserva in reservas:
            if seleccion in reserva.habitaciones_ids:
                reservas_habitacion.append(reserva)
        
        limpiar_pantalla()
        print("=" * 50)
        print(f"  RESERVAS DE LA HABITACIÓN {seleccion}")
        print("=" * 50)
        
        if not reservas_habitacion:
            print(f"\n  No hay reservas para la habitación {seleccion}.")
        else:
            for i, reserva in enumerate(reservas_habitacion, 1):
                noches = (reserva.check_out - reserva.check_in).days
                print(f"\n  [{i}] Cliente: {reserva.cliente}")
                print(f"      Fechas: {reserva.check_in.strftime('%d-%m-%Y')} → {reserva.check_out.strftime('%d-%m-%Y')} ({noches} noches)")
                if reserva.servicios_nombres:
                    servicios_texto = ', '.join(reserva.servicios_nombres)
                    print(f"      Servicios: {servicios_texto}")
                else:
                    print(f"      Servicios: Ninguno")
        
        print("\n" + "=" * 50)
        pausa()

def ver_servicios_interfaz():
    limpiar_pantalla()
    print("╔══════════════════════════════════════╗")
    print("║         SERVICIOS DEL HOTEL          ║")
    print("╠══════════════════════════════════════╣")
    print("║                                      ║")
    print("║  1. DESAYUNO                         ║")
    print("║     • Capacidad total: 5 personas    ║")
    print("║                                      ║")
    print("║  2. MASAJE                           ║")
    print("║     • Capacidad total: 3 personas    ║")
    print("║                                      ║")
    print("║  3. YOGA                             ║")
    print("║     • Capacidad total: 3 personas    ║")
    print("╚══════════════════════════════════════╝")
    print()
    print("Nota: La suite H204 incluye desayuno obligatorio.")
    print("      No se pueden reservar masaje y yoga en la misma estancia.")
    input("\nPresiona Enter para volver al menú")

def solicitar_cliente():
    while True:
        limpiar_pantalla()
        print("NUEVA RESERVA")
        print("Escribe 'cancelar' en cualquier momento para salir.\n")
    
        nombre = input("Nombre del cliente: ").strip()
        if nombre.lower() == "cancelar":
            print("\nReserva cancelada.")
            return None
        valido, mensaje = validar_nombre(nombre)
        if valido:
            return nombre
    
        print(f"\n Error: {mensaje}")
        print("Intenta de nuevo.\n")
        pausa()

def solicitar_fechas():
    # Check-in
    while True:
        limpiar_pantalla()
        print("Introduce las fechas de la reserva. Formato: DD-MM-AAAA")
        print("Escribe 'cancelar' en cualquier momento para salir.\n")
    
        entrada = input("Check-in (DD-MM-AAAA) o 'cancelar': ").strip()
        if entrada.lower() == "cancelar":
            return None, None
        try:
            dia, mes, anio = map(int, entrada.split('-'))
            check_in = date(anio, mes, dia)
            valido, msg = validar_check_in(check_in)
            if not valido:
                print(f"Error: {msg}")
                pausa()
                continue
            break
        except ValueError:
            print("Formato incorrecto. Usa DD-MM-AAAA.")
            pausa()
            continue
    
     # Check-out
    while True:
        limpiar_pantalla()
        print(f"CHECK-IN: {check_in.strftime('%d-%m-%Y')}")
        print("Introduce la fecha o 'cancelar' para salir")
        print()
        print("CHECK-OUT")
        
        entrada = input("   Fecha (DD-MM-AAAA): ").strip()
        if entrada.lower() == "cancelar":
            return None, None
        try:
            dia, mes, anio = map(int, entrada.split('-'))
            check_out = date(anio, mes, dia)
            valido, msg = validar_check_out(check_in, check_out)
            if not valido:
                print(f" Error: {msg}")
                pausa()
                continue
            break
        except ValueError:
            print(" Formato incorrecto. Usa DD-MM-AAAA.")
            pausa()
            continue
    
    # Resumen de fechas
    noches = (check_out - check_in).days
    limpiar_pantalla()
    print("\n" + "="*30)
    print("FECHAS CONFIRMADAS")
    print("="*30)
    print(f"Check-in:  {check_in.strftime('%d-%m-%Y')}")
    print(f"Check-out: {check_out.strftime('%d-%m-%Y')}")
    print(f"Noches:    {noches}")
    pausa()
    return check_in, check_out

def solicitar_habitaciones(habitaciones, reservas, check_in, check_out, servicios):
   
    # Obtener disponibles
    disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios)
    if not disponibles:
        print("\n No hay habitaciones disponibles en esas fechas.")
        pausa()
        return None

    # Obtener disponibilidad de servicios para mostrar
    desayunos_disp = verificar_disponibilidad_servicio("desayuno", check_in, check_out, servicios, reservas)
    masajes_disp = verificar_disponibilidad_servicio("masaje", check_in, check_out, servicios, reservas)
    yogas_disp = verificar_disponibilidad_servicio("yoga", check_in, check_out, servicios, reservas)

    # Bucle de seleccion
    while True:
        limpiar_pantalla()
        print(f"HABITACIONES DISPONIBLES ({check_in.strftime('%d-%m-%Y')} al {check_out.strftime('%d-%m-%Y')})")
        print("=" * 50)

        # Mostrar por pisos
        print("\nPISO 1:")
        for hab in disponibles:
            if hab.piso == 1:
                suite_texto = " (REQUIERE DESAYUNO OBLIGATORIO)" if hab.id == "H204" else ""
                vista_texto = "Vista al mar" if hab.vista_mar else "Sin vista al mar"
                print(f"  • {hab.id} ({hab.tipo}) - {vista_texto}{suite_texto}")

        print("\nPISO 2:")
        for hab in disponibles:
            if hab.piso == 2:
                suite_texto = " (REQUIERE DESAYUNO OBLIGATORIO)" if hab.id == "H204" else ""
                vista_texto = "Vista al mar" if hab.vista_mar else "Sin vista al mar"
                print(f"  • {hab.id} ({hab.tipo}) - {vista_texto}{suite_texto}")

        # Mostrar disponibilidad de servicios
        print(f" Desayunos disponibles: {desayunos_disp}")
        print(f" Masajes disponibles: {masajes_disp}")
        print(f" Yoga disponibles: {yogas_disp}")

        print("\n" + "=" * 50)
        print("SELECCIÓN DE HABITACIONES")
        print("=" * 50)
        print("Máximo 2 habitaciones, y deben estar en el mismo piso.")
        print("Ingresa los IDs separados por comas (ejemplo: H101,H104)")
        print("O escribe 'cancelar' para salir.")

        entrada = input("\n>> ").strip().upper()
        if entrada.lower() == "cancelar":
            print("Selección cancelada.")
            return None

        # Procesar IDs
        ids = [id_.strip() for id_ in entrada.split(',') if id_.strip()]
        if not ids:
            print("No ingresaste ningún ID.")
            pausa()
            continue

        # validar restricciones
        valido, mensaje, habitaciones_validas = validar_restricciones_habitaciones(
            ids, habitaciones, reservas, check_in, check_out, servicios
        )

        if not valido:
            print(f"\n Error: {mensaje}")
            pausa()
            continue

        # Mostrar confirmacion
        limpiar_pantalla()
        print("\n Habitaciones seleccionadas:")
        for hab in habitaciones_validas:
            suite_texto = " (requiere desayuno)" if hab.id == "H204" else ""
            vista_texto = "Vista al mar" if hab.vista_mar else "Sin vista al mar"
            print(f"  • {hab.id} ({hab.tipo}) - Piso {hab.piso} - {vista_texto}{suite_texto}")

        respuesta = input("\n¿Confirmar estas habitaciones? (si/no): ").strip().lower()
        if respuesta == "si" or respuesta == "sí":
            return ids
        else:
            print("Selección cancelada. Intenta de nuevo.")
            pausa()

def solicitar_servicios(habitaciones_ids, check_in, check_out, servicios, reservas):
    
    servicios_seleccionados = []
    total_hab = len(habitaciones_ids)
    tiene_suite = "H204" in habitaciones_ids

    # Desayuno
    limpiar_pantalla()
    print("SERVICIO DE DESAYUNO")
    print("=" * 30)
    desayunos_disp = verificar_disponibilidad_servicio("desayuno", check_in, check_out, servicios, reservas)
    print(f"Desayunos disponibles: {desayunos_disp}\n")

    if tiene_suite:
        # Obligatorio al menos 1
        servicios_seleccionados.append("desayuno:1")
        print(" Desayuno obligatorio para la suite H204 (1 servicio).")
        if total_hab == 2:
            while True:
                limpiar_pantalla()
                print("SERVICIO DE DESAYUNO")
                print("=" * 30)
                print(f"Desayunos disponibles: {desayunos_disp}")
                print("(ya tienes 1 desayuno obligatorio para la suite H204)")
                print()
                resp = input("¿Añadir desayuno para la otra habitación? (si/no/cancelar): ").strip().lower()
                if resp in ("si", "sí", "no", "cancelar"):
                    break
                print("Respuesta no válida. Escribe 'si', 'no' o 'cancelar'.")
                pausa()

            if resp == "cancelar":
                print("\nOperación cancelada por el usuario.")
                return None
            if resp == "si":
                if desayunos_disp >= 2:
                    servicios_seleccionados = ["desayuno:2"]
                    print(" Desayuno para ambas habitaciones (2 servicios).")
                else:
                    print(f"No hay suficientes desayunos para ambas (solo {desayunos_disp} disponibles).")
                    print("Continuando solo con el desayuno obligatorio de la suite.")
            else:
                print("Sin desayuno adicional.")
    else:
        # Sin suite
        if total_hab == 1:
            while True:
                limpiar_pantalla()
                print("SERVICIO DE DESAYUNO")
                print("=" * 30)
                print(f"Desayunos disponibles: {desayunos_disp}\n")
                resp = input("¿Incluir desayuno? (si/no/cancelar): ").strip().lower()
                if resp in ("si", "sí", "no", "cancelar"):
                    break
                print("Respuesta no válida. Escribe 'si', 'no' o 'cancelar'.")
                pausa() 
            
            if resp == "cancelar":
                print("\nOperación cancelada por el usuario.")
                return None
            
            if resp == "si":
                if desayunos_disp >= 1:
                    servicios_seleccionados.append("desayuno:1")
                    print(" Desayuno añadido (1 servicio).")
                else:
                    print("No hay desayunos disponibles.")
            else:
                print("Sin desayuno.")
        else:  # 2 habitaciones sin suite
            while True:
                limpiar_pantalla()
                print("SERVICIO DE DESAYUNO")
                print("=" * 30)
                print(f"Desayunos disponibles: {desayunos_disp}\n")
                entrada = input("Cantidad de desayunos (0, 1 o 2) o 'cancelar': ").strip()

                if entrada.lower() == "cancelar":
                    print("\nOperación cancelada por el usuario.")
                    return None
                try:
                    cantidad = int(entrada)
                    if cantidad < 0 or cantidad > 2:
                        print("Debe ser 0, 1 o 2.")
                        pausa()
                        continue
                    if cantidad > desayunos_disp:
                        print(f"No hay suficientes desayunos (solo {desayunos_disp} disponibles).")
                        pausa()
                        continue
                    if cantidad > 0:
                        servicios_seleccionados.append(f"desayuno:{cantidad}")
                        print(f" Desayuno añadido ({cantidad} servicio(s)).")
                    else:
                        print("Sin desayuno.")
                    break
                except ValueError:
                    print("Ingresa un número (0, 1 o 2).")
                    pausa()
    pausa()

    # Calcular disponibilidad de ambos
    masajes_disp = verificar_disponibilidad_servicio("masaje", check_in, check_out, servicios, reservas)
    yogas_disp = verificar_disponibilidad_servicio("yoga", check_in, check_out, servicios, reservas)

    while True:
        limpiar_pantalla()
        print("SERVICIO EXTRA (MASAJE O YOGA)")
        print("=" * 30)
        print(f"Masajes disponibles: {masajes_disp}")
        print(f"Yoga disponibles:    {yogas_disp}\n")
        print("Puedes elegir entre masaje o yoga, pero no ambos.")
        print("También puedes optar por ninguno.\n")
        opcion = input("¿Qué deseas? (masaje / yoga / ninguno) [m/y/n]: ").strip().lower()

        if opcion in ("ninguno", "n"):
            print("Sin servicio extra.")
            break

        if opcion in ("masaje", "m"):
            servicio_elegido = "masaje"
            disponibilidad = masajes_disp
        elif opcion in ("yoga", "y"):
            servicio_elegido = "yoga"
            disponibilidad = yogas_disp
        else:
            print("Opción no válida. Escribe 'm', 'y' o 'n'.")
            pausa()
            continue

        if disponibilidad == 0:
            print(f"Lo siento, no hay {servicio_elegido} disponible en esas fechas.")
            pausa()
            continue

        # Preguntar cantidad (máximo: número de habitaciones y disponibilidad)
        max_cantidad = min(total_hab, disponibilidad)
        while True:
            entrada = input(f"Cantidad de {servicio_elegido} (máximo {max_cantidad}) o 'cancelar': ").strip()
            if entrada.lower() == "cancelar":
                print("\nOperación cancelada por el usuario.")
                return None
            try:
                cantidad = int(entrada)
                if cantidad < 1 or cantidad > max_cantidad:
                    print(f"Debe ser entre 1 y {max_cantidad}.")
                    pausa()
                    continue
                # Añadir servicio
                servicios_seleccionados.append(f"{servicio_elegido}:{cantidad}")
                print(f" {servicio_elegido.capitalize()} añadido ({cantidad} servicio(s)).")
                break
            except ValueError:
                print("Ingresa un número válido.")
                pausa()
        break   # Salir del bucle principal

    pausa()
    return servicios_seleccionados

def mostrar_resumen(cliente, check_in, check_out, habitaciones_ids, servicios_seleccionados):
    limpiar_pantalla()
    print("=" * 50)
    print("RESUMEN DE RESERVA")
    print("=" * 50)
    print(f"Cliente: {cliente}")
    print(f"Check-in:  {check_in.strftime('%d-%m-%Y')}")
    print(f"Check-out: {check_out.strftime('%d-%m-%Y')}")
    print(f"Noches:    {(check_out - check_in).days}")
    print(f"Habitaciones: {', '.join(habitaciones_ids)}")
    if servicios_seleccionados:
        print("Servicios:")
        for s in servicios_seleccionados:
            nombre, cant = s.split(":")
            print(f"  - {nombre.capitalize()}: {cant}")
    else:
        print("Servicios: Ninguno")
    print("=" * 50)

def mostrar_reservas_interfaz(reservas):
    """Muestra todas las reservas existentes en formato simple."""
    limpiar_pantalla()
    print("=" * 50)
    print("RESERVAS EXISTENTES")
    print("=" * 50)
    
    if not reservas:
        print("\nNo hay reservas registradas.")
    else:
        for i, reserva in enumerate(reservas, 1):
            print(f"\n[{i}] Cliente: {reserva.cliente}")
            print(f"    Fechas: {reserva.check_in.strftime('%d-%m-%Y')} al {reserva.check_out.strftime('%d-%m-%Y')}")
            print(f"    Habitaciones: {', '.join(reserva.habitaciones_ids)}")
            
            if reserva.servicios_nombres:
                print(f"    Servicios: {', '.join(reserva.servicios_nombres)}")
            else:
                print("    Servicios: Ninguno")
    
    print(f"\nTotal: {len(reservas)} reserva(s) activa(s)")
    print("=" * 50)
    pausa()

def crear_reserva_interfaz(habitaciones, servicios, reservas):
    limpiar_pantalla()
    
    #Cliente
    cliente = solicitar_cliente()
    if cliente is None:
        return
    
    #Fechas
    check_in, check_out = solicitar_fechas()
    if check_in is None:
        print("Reserva cancelada.")
        pausa()
        return
    
    #Habitaciones
    habitaciones_ids = solicitar_habitaciones(habitaciones, reservas, check_in, check_out, servicios)
    if habitaciones_ids is None:
        print("Reserva cancelada.")
        pausa()
        return

    #Servicios
    servicios_seleccionados = solicitar_servicios(habitaciones_ids, check_in, check_out, servicios, reservas)
    if servicios_seleccionados is None:
        print("Reserva cancelada.")
        pausa()
        return

    #Resumen y confirmacion
    while True:
        mostrar_resumen(cliente, check_in, check_out, habitaciones_ids, servicios_seleccionados)
        resp = input("\n¿Confirmar la reserva? (si/no/cancelar): ").strip().lower()
        if resp in ("si", "sí", "no", "cancelar"):
            break
        print("Respuesta no válida. Escribe 'si', 'no' o 'cancelar'.")
        pausa()

    if resp == "cancelar":
        print("\nReserva cancelada por el usuario.")
        pausa()
        return

    if resp == "si":
        exito, msg, nueva_reserva = crear_reserva_sistema(
            cliente, habitaciones_ids, servicios_seleccionados,
            check_in, check_out, habitaciones, servicios, reservas
        )
        if exito:
            from guardar_y_cargar import guardar_datos
            guardar_datos(habitaciones, servicios, reservas)
            print("\n¡Reserva creada exitosamente!")
            print(f"ID de reserva: {len(reservas)}")
        else:
            print(f"\nError: {msg}")
    else:
        print("\nReserva cancelada por el usuario.")
    
    pausa()

def cancelar_reserva_interfaz(reservas, habitaciones, servicios):

    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("                   CANCELAR RESERVA")
        print("=" * 60)
        
        # Verificar si hay reservas
        if not reservas:
            print("\n    No hay reservas para cancelar.")
            pausa()
            return
        
        # Mostrar lista de reservas
        for i, reserva in enumerate(reservas, 1):
            print(f"\n  [{i}] Cliente: {reserva.cliente}")
            print(f"         {reserva.check_in.strftime('%d-%m-%Y')} → {reserva.check_out.strftime('%d-%m-%Y')}")
            print(f"         Habitaciones: {', '.join(reserva.habitaciones_ids)}")
        
        print("\n" + "=" * 60)
        
        entrada = input("\nIngresa el número de reserva a cancelar (o '0' para salir): ").strip()

        if entrada == "0" or entrada.lower() == "cancelar":
                    print("\nOperación cancelada.")
                    pausa()
                    return

        # Seleccionar reserva
        try:    
            numero = int(entrada)
                
            if numero < 1 or numero > len(reservas):
                print(f"  Número inválido. Debe ser entre 1 y {len(reservas)}.")
                pausa()
                continue
            break
                
        except ValueError:
            print("  Por favor, ingresa un número válido.")
            pausa()
            continue
        
     # Mostrar detalles de la reserva seleccionada
    indice = numero - 1
    reserva_seleccionada = reservas[indice]

    while True: 
        limpiar_pantalla()
        print("=" * 60)
        print("              RESERVA SELECCIONADA")
        print("=" * 60)
        print(f"\n  Cliente: {reserva_seleccionada.cliente}")
        print(f"   {reserva_seleccionada.check_in.strftime('%d-%m-%Y')} → {reserva_seleccionada.check_out.strftime('%d-%m-%Y')}")
        print(f"   Habitaciones: {', '.join(reserva_seleccionada.habitaciones_ids)}")
            
        if reserva_seleccionada.servicios_nombres:
            servicios_legibles = []
            for servicio in reserva_seleccionada.servicios_nombres:
                nombre, cantidad = servicio.split(":")
                servicios_legibles.append(f"{nombre.capitalize()} ({cantidad})")
            print(f"     Servicios: {', '.join(servicios_legibles)}")
        else:
            print("      Servicios: Ninguno")
            
        print("\n" + "=" * 60)
            
        # Confirmar cancelacion
        respuesta = input("\n¿Estás seguro de cancelar esta reserva? (si/no): ").strip().lower()
        if respuesta in ("si", "sí", "no"):
            break
        print("Respuesta no válida. Escribe 'si' o 'no'.")
        pausa()
        
    if respuesta == "si" or respuesta == "sí":
        # Eliminar reserva
        reservas.pop(indice)
            
        #   Guardar cambios
        guardar_datos(habitaciones, servicios, reservas)
            
        limpiar_pantalla()
        print("=" * 60)
        print("                     RESERVA CANCELADA")
        print("=" * 60)
        print("\n  La reserva ha sido cancelada exitosamente.")
        print("  Las habitaciones y servicios han sido liberados.")
        print("\n" + "=" * 60)
    else:
        print("\nOperación cancelada por el usuario.")
        
    pausa()

def buscar_hueco_interfaz(habitaciones, servicios, reservas):

    # Habitaciones
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("              BUSCAR HUECO AUTOMÁTICO")
        print("=" * 60)
        print("\nSelecciona las habitaciones (máximo 2, mismo piso)")
        print("IDs separados por comas (ejemplo: H101,H104)")
        print("O escribe 'cancelar' para salir.")
        entrada = input("\n>> ").strip().upper()
        
        if entrada.lower() == "cancelar":
            print("\nOperación cancelada.")
            pausa()
            return
        
        ids = [id_.strip() for id_ in entrada.split(',') if id_.strip()]
        if not ids:
            print("No ingresaste ningún ID.")
            pausa()
            continue
        
        if len(ids) > 2:
            print("Máximo 2 habitaciones.")
            pausa()
            continue
        
        #existencia y mismo piso
        habitaciones_validas = []
        piso_anterior = None
        valido = True
        for id_hab in ids:
            hab_obj = None
            for h in habitaciones:
                if h.id == id_hab:
                    hab_obj = h
                    break
            if not hab_obj:
                print(f"La habitación '{id_hab}' no existe.")
                valido = False
                break
            if piso_anterior is None:
                piso_anterior = hab_obj.piso
            elif hab_obj.piso != piso_anterior:
                print("Las habitaciones deben estar en el mismo piso.")
                valido = False
                break
            habitaciones_validas.append(hab_obj)
        
        if not valido:
            pausa()
            continue
        
        habitaciones_ids = ids
        break
    
    #Servicios
    servicios_seleccionados = []
    total_hab = len(habitaciones_ids)
    
    # Desayuno
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("              DESAYUNO")
        print("=" * 60)
        print(f"Habitaciones seleccionadas: {', '.join(habitaciones_ids)}")
        print(f"Puedes pedir hasta {total_hab} desayunos.\n")
        
        if "H204" in habitaciones_ids:
            min_desayuno = 1
        else:
            min_desayuno = 0
        max_desayuno = total_hab

        entrada = input(f"Cantidad de desayunos ({min_desayuno} - {max_desayuno}) o 'cancelar': ").strip()
        if entrada.lower() == "cancelar":
            print("\nOperación cancelada.")
            pausa()
            return
        try:
            cantidad = int(entrada)
            if cantidad < min_desayuno or cantidad > max_desayuno:
                print(f"Debe ser entre {min_desayuno} y {max_desayuno}.")
                pausa()
                continue
            if cantidad > 0:
                servicios_seleccionados.append(f"desayuno:{cantidad}")
            break
        except ValueError:
            print("Ingresa un número válido.")
            pausa()
    
    #Masaje o yoga
    servicio_extra = None
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("              SERVICIO EXTRA (MASAJE O YOGA)")
        print("=" * 60)
        print(f"Habitaciones seleccionadas: {', '.join(habitaciones_ids)}")
        print("Elige entre masaje o yoga, o ninguno.\n")
        opcion = input("¿Qué deseas? (masaje / yoga / ninguno) [m/y/n]: ").strip().lower()
        if opcion in ("ninguno", "n"):
            print("Sin servicio extra.")
            break
        elif opcion in ("masaje", "m"):
            servicio_extra = "masaje"
            break
        elif opcion in ("yoga", "y"):
            servicio_extra = "yoga"
            break
        else:
            print("Opción no válida. Escribe 'm', 'y' o 'n'.")
            pausa()
            continue

    if servicio_extra:
        max_cantidad = total_hab
        while True:
            entrada = input(f"Cantidad de {servicio_extra} (máximo {max_cantidad}) o 'cancelar': ").strip()
            if entrada.lower() == "cancelar":
                print("\nOperación cancelada.")
                pausa()
                return
            try:
                cantidad = int(entrada)
                if cantidad < 1 or cantidad > max_cantidad:
                    print(f"Debe ser entre 1 y {max_cantidad}.")
                    pausa()
                    continue
                servicios_seleccionados.append(f"{servicio_extra}:{cantidad}")
                print(f" {servicio_extra.capitalize()} añadido ({cantidad} servicio(s)).")
                break
            except ValueError:
                print("Ingresa un número válido.")
                pausa()
    
    # Cantidad de noches
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("              DURACIÓN DE LA ESTANCIA")
        print("=" * 60)
        print(f"Habitaciones: {', '.join(habitaciones_ids)}")
        print(f"Servicios: {', '.join(servicios_seleccionados) if servicios_seleccionados else 'Ninguno'}\n")
        
        entrada = input("Número de noches (mínimo 1) o 'cancelar': ").strip()
        if entrada.lower() == "cancelar":
            print("\nOperación cancelada.")
            pausa()
            return
        try:
            noches = int(entrada)
            if noches < 1:
                print("Debe ser al menos 1 noche.")
                pausa()
                continue
            break
        except ValueError:
            print("Ingresa un número válido.")
            pausa()
    
    #Buscamos
    print("\nBuscando disponibilidad...")
    check_in, check_out = buscar_hueco_automatico(
        habitaciones_ids, servicios_seleccionados, noches,
        habitaciones, servicios, reservas
    )
    
    limpiar_pantalla()
    if check_in is None:
        print("=" * 60)
        print("              NO SE ENCONTRÓ DISPONIBILIDAD")
        print("=" * 60)
        print("\nNo hay fechas disponibles para tus requisitos en los próximos 2 años.")
        pausa()
        return
    
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("              HUECO ENCONTRADO")
        print("=" * 60)
        print(f"\n  Check-in:  {check_in.strftime('%d-%m-%Y')}")
        print(f"  Check-out: {check_out.strftime('%d-%m-%Y')}")
        print(f"  Noches:    {noches}")
        print(f"  Habitaciones: {', '.join(habitaciones_ids)}")
        if servicios_seleccionados:
            print(f"  Servicios: {', '.join(servicios_seleccionados)}")
        else:
            print("  Servicios: Ninguno")
        print("\n" + "=" * 60)
        
        resp = input("\n¿Deseas crear una reserva con estas fechas? (si/no): ").strip().lower()
        if resp in ("si", "sí", "no"):
            break
        print("Respuesta no válida. Escribe 'si' o 'no'.")
        pausa()
    
    if resp == "no":
        print("\nOperación cancelada.")
        pausa()
        return
    
    #Pedmos cliente
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("              CREAR RESERVA")
        print("=" * 60)
        print(f"Fechas: {check_in.strftime('%d-%m-%Y')} → {check_out.strftime('%d-%m-%Y')}")
        print(f"Habitaciones: {', '.join(habitaciones_ids)}\n")
        
        cliente = input("Nombre del cliente (o 'cancelar'): ").strip()
        if cliente.lower() == "cancelar":
            print("\nReserva cancelada.")
            pausa()
            return
        valido, mensaje = validar_nombre(cliente)
        if valido:
            break
        
        print(f"Error: {mensaje}")
        pausa()
    
    exito, msg, nueva_reserva = crear_reserva_sistema(
        cliente, habitaciones_ids, servicios_seleccionados,
        check_in, check_out, habitaciones, servicios, reservas
    )
    
    if exito:
        guardar_datos(habitaciones, servicios, reservas)
        limpiar_pantalla()
        print("=" * 60)
        print("              ¡RESERVA CREADA EXITOSAMENTE!")
        print("=" * 60)
        print(f"\n  Cliente: {cliente}")
        print(f"  Fechas: {check_in.strftime('%d-%m-%Y')} → {check_out.strftime('%d-%m-%Y')}")
        print(f"  Habitaciones: {', '.join(habitaciones_ids)}")
        if servicios_seleccionados:
            print(f"  Servicios: {', '.join(servicios_seleccionados)}")
        print("\n" + "=" * 60)
    else:
        print(f"\nError: {msg}")
    
    pausa()
