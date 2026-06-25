# 1. Qué hace el programa y cómo lo diseñé.

Mi programa es un **sistema de gestión de reservas de un hotel**. En general sirve para planificar y administrar las reservas de las habitaciones y servicios disponibles para cada habitación de forma organizada, evitando conflictos en la disponibilidad de estos servicios y siguiendo una serie de restricciones que cada reserva tiene que respetar.

Para ejecutar el programa se usa la interfaz de la consola que está diseñada para ser interactiva y guiada paso a paso sin ningún problema.

## 1.1 El dominio: Hotel "Blue Gate" 

Un hotel es un dominio sencillo para poder cumplir con los requisitos del proyecto. En general el hotel cuenta con:

- **8 habitaciones** distribuidas en dos pisos, con diferentes tipos y vistas.
- **3 servicios adicionales**: desayuno, masaje y yoga, cada uno con una capacidad limitada.
- **Sus respectivas reglas** que deben de cumplirse para reservar correctamente.

## 1.2 El evento : Reserva de habitaciones

El evento principal del programa sería la reserva de habitaciones. Cada reserva tiene: 

 **Cliente** : Nombre de la persona que hace la reserva
 **Habitaciones** : Lista de IDs de habitaciones reservadas (["H101", "H104"])
 **Servicios** | Lista de servicios adicionales solicitados (["desayuno:1", "masaje:1"])
 **Check-in** | Fecha de inicio de la estancia (15-07-2026)
 **Check-out** | Fecha de fin de la estancia (20-07-2026 )

## 1.3 Los recursos: Habitaciones y servicios
Hay un total de 8 habitaciones y cada habitación tiene tres atributos:

 **Tipo** | Simple / Doble / Suite |
 **Vista al mar** | Sí / No |
 **Piso** | 1 / 2 |

En cuanto a los servicios son 3 tipos de servicios y cada uno con su disponibilidad simultánea (o sea que si en x día están ocupados los 5 desayunos para ese día quedan 0 desayunos disponibles):

 | **Desayuno** | 5 unidades | 1 por habitación |
 | **Masaje** | 3 unidades | 1 por habitación |
 | **Yoga** | 3 unidades | 1 por habitación |

## 1.4 Las Restricciones personalizadas:

### 1.4.1 La suite H204 requiere 1 desayuno disponible para poder ser reservada

### 1.4.2 El servicio de masaje y el servicio de yoga no es posible reservarlos simultáneamente.

Para el diseño del programa como tal decidí partir del menú inicial del sistema de reservas, al cual fui añadiendo y quitando cosas hasta que al final quedaron las 7 opciones siguientes: 

 ("╔══════════════════════════════════════════════╗")
 ("║     BLUE GATE HOTEL - Sistema de Reservas    ║")
 ("╠══════════════════════════════════════════════╣")
 ("║                                              ║")
 ("║   1. Ver catálogo de habitaciones            ║")
 ("║   2. Ver catálogo de servicios               ║")
 ("║   3. Ver reservas existentes                 ║")
 ("║   4. Crear nueva reserva                     ║")
 ("║   5. Buscar hueco automático                 ║")
 ("║   6. Cancelar reserva existente              ║")
 ("║   7. Salir                                   ║")
 ("║                                              ║")
 ("╚══════════════════════════════════════════════╝")

Cada opción está implementada en el código siguiendo (aproximadamente) el mismo orden. Además se encarga de que no hallan conflicto con los recursos que tenemos, que no se viole la cantidad de los mismos (principalmente de los servicios que tienen cantidad máxima cada uno de ellos para gestionarla como queramos) y por último que se cumplan las restricciones correctamente. 

En cuanto a **la creación del evento**, tanto la opción 4 (creación manual) y la 6 (Buscar automáticamente) se encargan de la creación de los mismos.

-**Creación manual (opción 4)** | Guía al usuario paso a paso para crear una reserva, validando disponibilidad y restricciones. |
-**Búsqueda automática(opción 5)** | Encuentra automáticamente la primera fecha disponible para las habitaciones y servicios solicitados. |

(Al final pondré ejemplos del flujo de los más importantes (Opción 4,5,6))

## 1.5 Estructura del código

Para organizar el proyecto, decidí separar el código en diferentes archivos según su responsabilidad. Esta decisión fue clave para mantener el código limpio y fácil de modificar.

- **Clases.py**: Aquí defino las clases que utilizaré en el proyecto (Habitación, Servicio, Reserva).
- **logica_reservas.py**: Contiene funciones con lógicas necesarias para las funciones de la interfaz. Aquí están las funciones que validan disponibilidad, verifican restricciones y buscan huecos. Solamente recibe datos y devuelve resultados.
- **interfaz_usuario.py**: Maneja toda la interacción con el usuario. Muestra menús, pide datos y muestra resultados.
- **guardar_y_cargar.py**: Se encarga de la persistencia. Guarda y carga los datos del json.
- **Main.py**: Es el punto de entrada del programa. Contiene el bucle principal y el menú.

Esta estructura fue la mejor que se me ocurrió para el proyecto actualmente. Aunque la clase interfaz_usuario es mucho más larga que las demás realmente solo ocurre porque se encarga de manejar las entradas y salidas a la interfaz, pero en general se entiende bastante bien y está organizado.

# 2. Dificultades durante la creación.

## 2.1
El principal problema fue la **falta de organización** que derivó en unos cuantos problemas que tuve que solucionar poco a poco. Me enfoqué demasiado en lo que estaba haciendo en el momento y no miraba lo que tendría que hacer más adelante. Por esta razón cuando volví a abrir el proyecto hace poco tomé la decisión de rehacerlo. Obviamente no empecé desde 0, sino que reutilicé muchas funciones y lógicas así como clases básicas como por ejemplo "guardar_y_cargar" o "Clases".

La magnitud de aquel código espagueti hacía que modificar o añadir algo sea jodido. Llegué a tener varias clases que en realidad no era necesario tenerlas tan fragmentadas. Esto llegó a opacar la clase que manejaba la interfaz. Por esto tomé la decisión de reestructurar mis clases y mantener:

- **logica_reservas.py**: todas las funciones de validación y disponibilidad juntas las cuales solo reciben y retornan, con el objetivo de ser usadas por funciones de la interfaz

- **interfaz_usuario.py**: todas las funciones con las que el usuario va a interactuar.

Ahora en perspectiva es mucho más fácil leer el código y entenderlo. Además todo está ordenado y algunas funciones tienen algunos comentarios cortos para evitar perderse.

## 2.2
Otra cosa que me causó dudas fue el tema de la **persistencia de datos y el uso de json en general** para cargar y guardar datos a la escala de este proyecto. Fue a lo primero que me enfrenté a la hora de crear el programa. Habían detalles de los cuales simplemente no tenía casi práctica como por ejemplo convertir a string objetos date para poder guardarlos en json, etc.

## 2.3
El hecho de que la suite tenga requerimientos especificos con respecto a los desayunos me causo mas problemas de los que esperaba. Aunque casi todos eran casos esquinas este fue unos de los casos principales por los que decidi hacerle remake al proyecto. La mejor solucion fue trabajar cuidadosamente caso por caso.

## 2.4
Otro problema con el cual también me topé ya entrando en las fases finales fue **el manejo de las entradas del usuario en la interfaz**. La causa no fue más que el uso incorrecto de bucles tan sencillos como while true pero que durante la creación del código no tenía contemplado correctamente. Lo que solía suceder es que el usuario introducía algo incorrecto y a pesar de que el programa lo detectaba y notificaba bien, el mensaje quedaba grabado y sobrecargaba la interfaz. 

# 3. Qué aprendí luego de crearlo?

Esta respuesta está bastante ligado a lo anterior. De más está decir que lo que más me ha quedado claro es que nunca estás lo suficientemente organizado. Es crucial tener la mayor cantidad de cosas pensadas antes de comenzar, por lo menos desde lo más general hasta ir poco a poco centrándote en los detalles. Tener cuidado con las clases, porque a pesar de ser muy útiles si fragmentas cosas que no deben ser fragmentadas, por la naturaleza de su uso, se puede complicar mucho tanto la creación de código nuevo como la reutilización de código antiguo.

También tener muy en cuenta que está destinado a formar parte de la interfaz con la que el usuario va a interactuar. En esta parte del código las funciones deben estar pensadas para interactuar de la forma más fluida posible así que la utilización correcta de bucles es muy importante.

# 4. Cómo usar el programa?

Para iniciar, ejecutamos Main.py

El programa cargará los datos del json (aunque también preparé guardar_y_cargar para que cargue de 0 correctamente si el json está vacío).

Al ejecutarse aparecerá el menú con las 7 opciones que vimos anteriormente.
A continuación pondré ejemplos del flujo para un caso particular de las opciones 4,5 y 6 que 

## 4.1 Opción 4: Crear nueva reserva (Caso particular de Suite H204)

**Nombre del cliente**
NUEVA RESERVA
Escribe 'cancelar' en cualquier momento para salir.

Nombre del cliente: Juan Pérez

**Fechas de la estancia**
Introduce las fechas de la reserva. Formato: DD-MM-AAAA

Check-in (DD-MM-AAAA) o 'cancelar': 01-08-2026
Check-out (DD-MM-AAAA) o 'cancelar': 05-08-2026

Fechas confirmadas:
  Check-in:  01-08-2026
  Check-out: 05-08-2026
  Noches:    4

**Seleccionar Habitaciones**
HABITACIONES DISPONIBLES (01-08-2026 al 05-08-2026)
==================================================

PISO 1:
  • H101 (simple) - Sin vista al mar
  • H102 (simple) - Sin vista al mar
  • H103 (simple) - Sin vista al mar
  • H104 (doble) - Sin vista al mar

PISO 2:
  • H201 (simple) - Vista al mar
  • H202 (simple) - Sin vista al mar
  • H203 (doble) - Vista al mar
  • H204 (suite) - Vista al mar (REQUIERE DESAYUNO OBLIGATORIO)

Desayunos disponibles: 5
Masajes disponibles: 3
Yoga disponibles: 3

SELECCIÓN DE HABITACIONES
Máximo 2 habitaciones, y deben estar en el mismo piso.
Ingresa los IDs separados por comas (ejemplo: H101,H104)

>> H204

**Confirmar habitaciones**
Habitaciones seleccionadas:
  • H204 (suite) - Piso 2 - Vista al mar (requiere desayuno)

¿Confirmar estas habitaciones? (si/no): si

**Seleccionar servicios**
SERVICIO DE DESAYUNO
==============================
Desayunos disponibles: 5

 Desayuno obligatorio para la suite H204 (1 servicio).

SERVICIO EXTRA (MASAJE O YOGA)
==============================
Masajes disponibles: 3
Yoga disponibles: 3

Puedes elegir entre masaje o yoga, pero no ambos.
¿Qué deseas? (masaje / yoga / ninguno) [m/y/n]: n

Sin servicio extra.

**Confirmación de la reserva**
==================================================
RESUMEN DE RESERVA
==================================================
Cliente: Juan Pérez
Check-in:  01-08-2026
Check-out: 05-08-2026
Noches:    4
Habitaciones: H204
Servicios:
  - Desayuno: 1
==================================================

¿Confirmar la reserva? (si/no/cancelar): si

¡Reserva creada exitosamente!
ID de reserva: 1

## 4.2 Opción 5: Buscar hueco automático (caso particular para H101 y H104)

**Habitaciones**
BUSCAR HUECO AUTOMÁTICO
Selecciona las habitaciones (máximo 2, mismo piso)
IDs separados por comas (ejemplo: H101,H104)

>> H101,H104

**Servicios**
DESAYUNO
============================================================
Habitaciones seleccionadas: H101, H104
Puedes pedir hasta 2 desayunos.

Cantidad de desayunos (0 - 2) o 'cancelar': 1

SERVICIO EXTRA (MASAJE O YOGA)
============================================================
Habitaciones seleccionadas: H101, H104
¿Qué deseas? (masaje / yoga / ninguno) [m/y/n]: m

Cantidad de masaje (máximo 2) o 'cancelar': 1

**Cantidad de noches**

DURACIÓN DE LA ESTANCIA
============================================================
Habitaciones: H101, H104
Servicios: desayuno:1, masaje:1

Número de noches (mínimo 1) o 'cancelar': 3

**Muestra el resultado de la búsqueda**
Buscando disponibilidad...

HUECO ENCONTRADO
============================================================
  Check-in:  10-08-2026
  Check-out: 13-08-2026
  Noches:    3
  Habitaciones: H101, H104
  Servicios: desayuno:1, masaje:1
============================================================

¿Deseas crear una reserva con estas fechas? (si/no): si
Nombre del cliente (o 'cancelar'): María García

¡RESERVA CREADA EXITOSAMENTE!
  Cliente: María García
  Fechas: 10-08-2026 → 13-08-2026
  Habitaciones: H101, H104
  Servicios: desayuno:1, masaje:1

## 4.3 Opción 6: Cancelar una reserva

**Se muestran las reservas activas**
============================================================
                   CANCELAR RESERVA
============================================================

  [1] Cliente: Juan Pérez
         01-08-2026 → 05-08-2026
         Habitaciones: H204

  [2] Cliente: María García
         10-08-2026 → 13-08-2026
         Habitaciones: H101, H104

============================================================

**Seleccionamos la reserva a cancelar**
Ingresa el número de reserva a cancelar (o '0' para salir): 1

**Confirmamos cancelación**
============================================================
              RESERVA SELECCIONADA
============================================================

  Cliente: Juan Pérez
   01-08-2026 → 05-08-2026
   Habitaciones: H204
     Servicios: Desayuno (1)

============================================================

¿Estás seguro de cancelar esta reserva? (si/no): si

============================================================
                     RESERVA CANCELADA
============================================================

  La reserva ha sido cancelada exitosamente.
  Las habitaciones y servicios han sido liberados.

============================================================