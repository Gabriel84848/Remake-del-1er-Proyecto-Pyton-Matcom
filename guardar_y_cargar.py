import json
from datetime import date
from pathlib import Path
from Clases import Habitacion, Servicio, Reserva


def cargar_datos():
    ruta = Path("Yeison.json")
    try:
        with ruta.open() as archivo:
            datos = json.load(archivo)

        lista_habitaciones = []
        for hab in datos["habitaciones"]:
            nueva_habitacion = Habitacion(
                hab["id"],
                hab["tipo"],
                hab["vista_mar"],
                hab["piso"]
            )
            lista_habitaciones.append(nueva_habitacion)

        lista_servicios = []
        for serv in datos["servicios"]:
            nuevo_serv = Servicio(
                serv["nombre"],
                serv["capacidad_total"]
            )
            lista_servicios.append(nuevo_serv)

        lista_reservas = []
        if "reservas" in datos:
            for res in datos["reservas"]:
                nueva_reserva = Reserva(
                    res["cliente"],
                    res["habitaciones"],
                    res["servicios"],
                    date.fromisoformat(res["check_in"]),   # Convertimos string → date
                    date.fromisoformat(res["check_out"])   # Convertimos string → date
                )
                lista_reservas.append(nueva_reserva)

        return lista_habitaciones, lista_servicios, lista_reservas

    except Exception:
        print("Error al cargar 'Yeison.json'. Usando datos por defecto.")

        habitaciones = [
            Habitacion("H101", "simple", False, 1),
            Habitacion("H102", "simple", False, 1),
            Habitacion("H103", "simple", False, 1),
            Habitacion("H104", "doble", False, 1),
            Habitacion("H201", "simple", True, 2),
            Habitacion("H202", "simple", False, 2),
            Habitacion("H203", "doble", True, 2),
            Habitacion("H204", "suite", True, 2)
        ]

        servicios = [
            Servicio("desayuno", 5),
            Servicio("masaje", 3),
            Servicio("yoga", 3)
        ]

        return habitaciones, servicios, []


def guardar_datos(habitaciones, servicios, reservas):
    ruta = Path("Yeison.json")

    datos = {}

    lista_habitaciones_dict = []
    for habitacion in habitaciones:
        habitacion_dict = {
            "id": habitacion.id,
            "tipo": habitacion.tipo,
            "vista_mar": habitacion.vista_mar,
            "piso": habitacion.piso
        }
        lista_habitaciones_dict.append(habitacion_dict)
    datos["habitaciones"] = lista_habitaciones_dict

    lista_servicios_dict = []
    for servicio in servicios:
        servicio_dict = {
            "nombre": servicio.nombre,
            "capacidad_total": servicio.capacidad_total
        }
        lista_servicios_dict.append(servicio_dict)
    datos["servicios"] = lista_servicios_dict

    lista_reservas_dict = []
    for reserva in reservas:
        lista_reservas_dict.append(reserva.to_dict())
    datos["reservas"] = lista_reservas_dict

    with ruta.open("w") as archivo:
        json.dump(datos, archivo, indent=2)