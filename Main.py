import os
from guardar_y_cargar import cargar_datos
from interfaz_usuario import (
    limpiar_pantalla,
    crear_reserva_interfaz,
    ver_habitaciones_interfaz,
    ver_servicios_interfaz,
    mostrar_reservas_interfaz,
    cancelar_reserva_interfaz,
    buscar_hueco_interfaz
)

def menu():
    limpiar_pantalla()
    print("╔══════════════════════════════════════════════╗")
    print("║     BLUE GATE HOTEL - Sistema de Reservas    ║")
    print("╠══════════════════════════════════════════════╣")
    print("║                                              ║")
    print("║   1. Ver catálogo de habitaciones            ║")
    print("║   2. Ver catálogo de servicios               ║")
    print("║   3. Ver reservas existentes                 ║")
    print("║   4. Crear nueva reserva                     ║")
    print("║   5. Buscar hueco automático                 ║")
    print("║   6. Cancelar reserva existente              ║")
    print("║   7. Salir                                   ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    return input("\nSelecciona una opción (1-7): ")

def main():
    habitaciones, servicios, reservas = cargar_datos()
    while True:
        opcion = menu()
        if opcion == "1":
            ver_habitaciones_interfaz(reservas)
        elif opcion == "2":
            ver_servicios_interfaz()
        elif opcion == "3":
            mostrar_reservas_interfaz(reservas)
        elif opcion == "4":
            crear_reserva_interfaz(habitaciones, servicios, reservas)
        elif opcion == "5":
            buscar_hueco_interfaz(habitaciones, servicios, reservas)
        elif opcion == "6":
            cancelar_reserva_interfaz(reservas, habitaciones, servicios)
        elif opcion == "7":
            limpiar_pantalla()
            print("Saliste...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()