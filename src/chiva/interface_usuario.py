import os
from datetime import date

from logica import (
    NIVELES,
    buscar_chiva,
    calcular_informe,
    clasificar_nivel,
    convertir_entero,
    crear_chiva,
    fecha_siguiente,
    registrar_dia,
    simular_dias,
    validar_dias_simulados,
    validar_pasajeros,
    validar_rango_simulacion,
)

if os.name == "nt":
    os.system("")  # Activa los colores ANSI en la terminal de Windows


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    CIAN = "\033[96m"
    MAGENTA = "\033[95m"


COLORES_NIVEL = {
    "baja": C.ROJO,
    "regular": C.AMARILLO,
    "buena": C.VERDE,
    "alta": C.CIAN,
}

ANCHO = 62

NIVELES = ("baja", "regular", "buena", "alta")

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def linea(caracter="─"):
    print(C.DIM + caracter * ANCHO + C.RESET)


def encabezado(texto):
    print()
    print(C.BOLD + C.MAGENTA + f" ◆ {texto}" + C.RESET)
    linea()


def ok(texto):
    print(C.VERDE + "✔ " + texto + C.RESET)


def error(texto):
    print(C.ROJO + "✘ " + texto + C.RESET)


def pausar():
    input(C.DIM + "\nPresiona Enter para continuar..." + C.RESET)


def pedir(texto, defecto=None):
    sufijo = f" [{defecto}]" if defecto is not None else ""
    respuesta = input(f"{C.CIAN}➜ {texto}{sufijo}: {C.RESET}").strip()
    if respuesta == "" and defecto is not None:
        return str(defecto)
    return respuesta


def banner():
    print(C.BOLD + C.CIAN)
    print("  ╔" + "═" * (ANCHO - 2) + "╗")
    print("  ║" + "GESTOR DE CHIVAS".center(ANCHO - 2) + "║")
    print("  ║" + "control de pasajeros".center(ANCHO - 2) + "║")
    print("  ╚" + "═" * (ANCHO - 2) + "╝" + C.RESET)


def menu_principal():
    opciones = [
        ("1", "Crear chiva"),
        ("2", "Ver chivas"),
        ("3", "Registrar pasajeros de un día"),
        ("4", "Simular días"),
        ("5", "Ver informe"),
        ("0", "Salir"),
    ]
    for numero, texto in opciones:
        print(f"   {C.AMARILLO}{numero}{C.RESET}  {texto}")
    print()
    return input(f"{C.BOLD}Elige una opción ➜ {C.RESET}").strip()


def elegir_chiva(chivas):
    if not chivas:
        error("Todavía no hay chivas registradas.")
        return None
    for i, chiva in enumerate(chivas, start=1):
        print(
            f"   {C.AMARILLO}{i}{C.RESET}  {chiva.nombre}  "
            f"{C.DIM}({chiva.puestos} puestos, {len(chiva.pasajeros)} días){C.RESET}"
        )
    print()
    eleccion = convertir_entero(pedir("Número de la chiva"))
    if eleccion is None or not 1 <= eleccion <= len(chivas):
        error("Selección no válida.")
        return None
    return chivas[eleccion - 1]


def accion_crear(chivas):
    encabezado("Crear chiva")
    hoy = date.today()
    nombre = pedir("Nombre de la chiva")
    puestos = convertir_entero(pedir("Número de puestos"))
    anio = convertir_entero(pedir("Año de inicio", hoy.year))
    mes = convertir_entero(pedir("Mes de inicio (1-12)", hoy.month))
    dia = convertir_entero(pedir("Día de inicio", hoy.day))

    chiva, mensaje = crear_chiva(chivas, nombre, puestos, anio, mes, dia)
    if mensaje:
        error(mensaje)
    else:
        ok(f"Chiva '{chiva.nombre}' creada. Inicia el {chiva.fecha_inicio:%d/%m/%Y}.")
    pausar()


def accion_ver(chivas):
    encabezado("Chivas registradas")
    if not chivas:
        print("   (ninguna todavía)")
    for chiva in chivas:
        print(
            f"   ▸ {C.BOLD}{chiva.nombre}{C.RESET} · {chiva.puestos} puestos · "
            f"inicio {chiva.fecha_inicio:%d/%m/%Y} · {len(chiva.pasajeros)} días"
        )
    pausar()


def accion_registrar(chivas):
    encabezado("Registrar pasajeros")
    chiva = elegir_chiva(chivas)
    if chiva is None:
        pausar()
        return

    fecha = fecha_siguiente(chiva)
    print(f"\n   Fecha a registrar: {C.BOLD}{fecha:%d/%m/%Y}{C.RESET}")

    while True:
        valor = convertir_entero(pedir(f"Pasajeros (0 a {chiva.puestos})"))
        valor, mensaje = validar_pasajeros(chiva, valor)
        if mensaje is None:
            break
        error(mensaje)

    registrar_dia(chiva, valor)
    nivel = clasificar_nivel(valor, chiva.puestos)
    color = COLORES_NIVEL[nivel]
    ok(f"Día {fecha:%d/%m/%Y} registrado: {valor} pasajeros ({color}{nivel}{C.VERDE}).")
    pausar()

def accion_simular(chivas):
    encabezado("Simular días")
    chiva = elegir_chiva(chivas)
    if chiva is None:
        pausar()
        return

    dias = convertir_entero(pedir("¿Cuántos días simular?", 7))
    dias, mensaje = validar_dias_simulados(dias)
    if mensaje:
        error(mensaje)
        pausar()
        return

    minimo = convertir_entero(pedir("Mínimo de pasajeros", 0))
    maximo = convertir_entero(pedir("Máximo de pasajeros", chiva.puestos))

    mensaje = validar_rango_simulacion(minimo, maximo)
    if mensaje:
        error(mensaje)
    else:
        # Validación extra de rango de puestos
        if minimo is None or maximo is None or minimo < 0 or maximo > chiva.puestos:
            error(f"Los valores deben ser enteros entre 0 y {chiva.puestos}.")
        else:
            simular_dias(chiva, dias, minimo, maximo)
            ok(f"Se simularon {dias} días con pasajeros entre {minimo} y {maximo}.")
    pausar()


def accion_informe(chivas):
    encabezado("Informe")
    chiva = elegir_chiva(chivas)
    if chiva is None:
        pausar()
        return

    informe = calcular_informe(chiva)
    print()
    print(
        f"   {C.BOLD}{informe['nombre']}{C.RESET} · {informe['puestos']} puestos · "
        f"{informe['dias']} días registrados"
    )

    if informe["dias"] == 0:
        print(C.DIM + "   Aún no hay días registrados." + C.RESET)
        pausar()
        return

    linea()
    datos = [
        ("Total de pasajeros", informe["total"]),
        ("Promedio por día", informe["promedio"]),
        ("Ocupación promedio", f"{informe['porcentaje']} %"),
        ("Desviación estándar", informe["desviacion"]),
        ("Día con más pasajeros", f"{informe['fecha_max']:%d/%m/%Y}"),
        ("Día con menos pasajeros", f"{informe['fecha_min']:%d/%m/%Y}"),
    ]
    for etiqueta, valor in datos:
        print(f"   {etiqueta:<26}{C.BOLD}{valor}{C.RESET}")

    print(f"\n{C.BOLD}   Niveles de ocupación{C.RESET}")
    maximo = max(informe["niveles"].values()) or 1
    for nivel in NIVELES:
        cantidad = informe["niveles"][nivel]
        barra = "█" * round(cantidad / maximo * 30)
        color = COLORES_NIVEL[nivel]
        print(f"   {color}{nivel:<9}{C.RESET} {color}{barra}{C.RESET} {cantidad}")

    linea()
    if informe["racha_longitud"] > 0:
        print(
            f"   {C.ROJO}Racha de ocupación baja:{C.RESET} {informe['racha_longitud']} días "
            f"desde el {informe['racha_inicio']:%d/%m/%Y}"
        )
    else:
        print(f"   {C.VERDE}Sin rachas de ocupación baja.{C.RESET}")

    if informe["faltan"]:
        print(
            f"   {C.AMARILLO}Faltan {informe['faltan']} días por registrar{C.RESET} "
            f"({informe['primer_faltante']:%d/%m} al {informe['ultimo_faltante']:%d/%m/%Y})"
        )
    else:
        print(f"   {C.VERDE}Al día: último registro {informe['ultimo_dia']:%d/%m/%Y}.{C.RESET}")
    pausar()


def main():
    chivas = []
    while True:
        limpiar()
        banner()
        print(f"\n   Chivas registradas: {C.BOLD}{len(chivas)}{C.RESET}\n")
        opcion = menu_principal()

        if opcion == "1":
            accion_crear(chivas)
        elif opcion == "2":
            accion_ver(chivas)
        elif opcion == "3":
            accion_registrar(chivas)
        elif opcion == "4":
            accion_simular(chivas)
        elif opcion == "5":
            accion_informe(chivas)
        elif opcion == "0":
            print(f"\n{C.VERDE}¡Hasta luego!{C.RESET}\n")
            break
        else:
            error("Opción no válida.")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma cerrado.")