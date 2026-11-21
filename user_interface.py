from os import system

from business_logic import (
    buscar_chiva,
    crear_chiva,
    generar_informe,
    simular_dias,
    validar_pasajeros,
)


def leer_entero(mensaje):
    texto = input(mensaje)
    try:
        return int(texto)
    except ValueError:
        return None


def pedir_chiva(lista_chivas):
    nombre = input("Nombre de la chiva: ").strip()
    chiva = buscar_chiva(lista_chivas, nombre)
    if chiva is None:
        print("Error: no existe una chiva con ese nombre.")
    return chiva


def menu_crear(lista_chivas, nombres):
    print("\n--- Crear chiva ---")
    nombre = input("Nombre de la chiva: ")
    puestos = leer_entero("Número de puestos: ")
    año = leer_entero("Año: ")
    mes = leer_entero("Mes: ")
    dia = leer_entero("Día: ")

    error = crear_chiva(lista_chivas, nombres, nombre, puestos, año, mes, dia)
    if error is None:
        print("Chiva creada, sin días registrados.")
    else:
        print(error)


def menu_registrar(lista_chivas):
    print("\n--- Registrar pasajeros del día siguiente ---")
    chiva = pedir_chiva(lista_chivas)
    if chiva is None:
        return

    print(f"Día siguiente: {chiva.fecha_siguiente()}")
    while True:
        pasajeros = leer_entero("Pasajeros: ")
        if pasajeros is None:
            print("Error: los pasajeros deben ser un número entero.")
            continue
        error = validar_pasajeros(pasajeros, chiva.numero_de_puestos)
        if error is not None:
            print(error)
            continue
        chiva.registrar_dia(pasajeros)
        print("Día registrado.")
        return


def menu_simular(lista_chivas):
    print("\n--- Simular días ---")
    chiva = pedir_chiva(lista_chivas)
    if chiva is None:
        return

    dias = leer_entero("¿Cuántos días quieres simular? ")
    if dias is None:
        print("Error: el número de días debe ser un entero.")
        return
    if dias < 1:
        print("Error: se debe simular al menos un día.")
        return

    minimo = leer_entero("Pasajeros mínimos: ")
    if minimo is None:
        print("Error: los pasajeros deben ser un número entero.")
        return
    error = validar_pasajeros(minimo, chiva.numero_de_puestos)
    if error is not None:
        print(error)
        return

    maximo = leer_entero("Pasajeros máximos: ")
    if maximo is None:
        print("Error: los pasajeros deben ser un número entero.")
        return
    error = validar_pasajeros(maximo, chiva.numero_de_puestos)
    if error is not None:
        print(error)
        return

    error = simular_dias(chiva, dias, minimo, maximo)
    if error is None:
        print(f"Se simularon {dias} días para {chiva.nombre}.")
    else:
        print(error)

def menu_informe(lista_chivas):
    print("\n--- Informe de chiva ---")
    chiva = pedir_chiva(lista_chivas)
    if chiva is None:
        return

    info = generar_informe(chiva)
    if info["dias"] == 0:
        print(f"La chiva {info['nombre']} no tiene días registrados.")
        return

    print(f"Último día registrado: {info['ultimo_dia']}")
    niveles = info["niveles"]
    print(f"Chiva: {info['nombre']}")
    print(f"Puestos: {info['puestos']}")
    print(f"Días registrados: {info['dias']}")
    print(f"Pasajeros totales: {info['total']}")
    print(f"Promedio de pasajeros por día: {info['promedio']}")
    print(f"Porcentaje de ocupación: {info['porcentaje']}%")
    print(f"Desviación estándar: {info['desviacion']}")
    print(f"Día con más pasajeros: {info['fecha_max']}")
    print(f"Día con menos pasajeros: {info['fecha_min']}")
    print(f"Días en ocupación baja: {niveles['baja']}")
    print(f"Días en ocupación regular: {niveles['regular']}")
    print(f"Días en ocupación buena: {niveles['buena']}")
    print(f"Días en ocupación alta: {niveles['alta']}")

    if info["racha_longitud"] == 0:
        print("No tuvo ningún día en ocupación baja.")
    else:
        print(
            f"Racha más larga en ocupación baja: {info['racha_longitud']} días, "
            f"empieza el {info['racha_inicio']}"
        )

    if info["faltan"] == 0:
        print("El registro está al día.")
    else:
        print(f"Días sin registrar: {info['faltan']}")

def main():
    lista_chivas = []
    nombres = set()

    while True:
        system("cls")
        print("=====================================")
        print("Programa de registro de chivas")
        print("=====================================")
        print("1. Crear chiva")
        print("2. Registrar pasajeros del día siguiente")
        print("3. Simular días")
        print("4. Informe de chiva")
        print("5. Chiva con mayor y menor ocupación")
        print("6. Cargar chivas y pasajeros desde archivos")
        print("7. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            menu_crear(lista_chivas, nombres)
        elif opcion == "2":
            menu_registrar(lista_chivas)
        elif opcion == "3":
            menu_simular(lista_chivas)
        elif opcion == "4":
            menu_informe(lista_chivas)
        elif opcion == "5":
            menu_extremos(lista_chivas)
        elif opcion == "6":
            menu_cargar(lista_chivas, nombres)
        elif opcion == "7":
            print("Vaya loco")
            break
        else:
            print("Error: opción no válida.")

        input("\nPresiona Enter para volver al menú...")


if __name__ == "__main__":
    main()