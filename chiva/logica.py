import random
from datetime import date


NIVELES = ("baja", "regular", "buena", "alta")


class Chiva:
    def __init__(self, nombre, puestos, fecha_inicio):
        self.nombre = nombre
        self.puestos = puestos
        self.fecha_inicio = fecha_inicio
        self.pasajeros = []


def crear_chiva(chivas, nombre, puestos, anio, mes, dia):
    nombre = nombre.strip()
    if nombre == "":
        return None, "El nombre no puede estar vacío."

    for chiva in chivas:
        if chiva.nombre == nombre:
            return None, "Ya existe una chiva con ese nombre."

    if puestos is None or puestos < 1:
        return None, "Los puestos deben ser un número entero mayor que 0."

    if anio is None or mes is None or dia is None:
        return None, "La fecha no es válida."

    try:
        fecha_inicio = date(anio, mes, dia)
    except:
        return None, "La fecha no es válida."

    chiva = Chiva(nombre, puestos, fecha_inicio)
    chivas.append(chiva)
    return chiva, None


def buscar_chiva(chivas, nombre):
    for chiva in chivas:
        if chiva.nombre == nombre:
            return chiva
    return None


def fecha_siguiente(chiva):
    año = chiva.fecha_inicio.year
    mes = chiva.fecha_inicio.month
    dia = chiva.fecha_inicio.day

    for i in range(len(chiva.pasajeros)):
        dia = dia + 1
        try:
            date(año, mes, dia)
        except:
            dia = 1
            mes = mes + 1
            if mes > 12:
                mes = 1
                año = año + 1

    return date(año, mes, dia)


def validar_pasajeros(chiva, valor):
    if valor is None:
        return None, "Debes ingresar un número entero."
    if valor < 0 or valor > chiva.puestos:
        return None, "Los pasajeros deben estar entre 0 y " + str(chiva.puestos) + "."
    return valor, None


def registrar_dia(chiva, pasajeros):
    chiva.pasajeros.append(pasajeros)


def clasificar_nivel(pasajeros, puestos):
    if puestos == 0:
        return "baja"
    porcentaje = (pasajeros * 100) / puestos
    if porcentaje < 45:
        return "baja"
    if porcentaje < 70:
        return "regular"
    if porcentaje < 90:
        return "buena"
    return "alta"


def validar_dias_simulados(dias):
    if dias is None:
        return None, "Debes ingresar un número entero."
    if dias < 1:
        return None, "Se debe simular al menos un día."
    return dias, None


def validar_rango_simulacion(minimo, maximo):
    if minimo is None or maximo is None:
        return "Los valores deben ser números enteros."
    if minimo > maximo:
        return "El mínimo no puede ser mayor que el máximo."
    return None


def simular_dias(chiva, dias, minimo, maximo):
    for i in range(dias):
        pasajeros = random.randint(minimo, maximo)
        registrar_dia(chiva, pasajeros)


def calcular_informe(chiva):
    dias = len(chiva.pasajeros)

    if dias == 0:
        return {
            "nombre": chiva.nombre,
            "puestos": chiva.puestos,
            "dias": 0,
        }

    total = 0
    for p in chiva.pasajeros:
        total = total + p

    promedio = total / dias
    porcentaje = round((promedio / chiva.puestos) * 100, 2)

    suma_cuadrados = 0
    for p in chiva.pasajeros:
        diferencia = p - promedio
        suma_cuadrados = suma_cuadrados + diferencia * diferencia
    desviacion = round((suma_cuadrados / dias) ** 0.5, 2)

    # Generar las fechas de cada día
    fechas = []
    año = chiva.fecha_inicio.year
    mes = chiva.fecha_inicio.month
    dia = chiva.fecha_inicio.day
    for i in range(dias):
        fechas.append(date(año, mes, dia))
        dia = dia + 1
        try:
            date(año, mes, dia)
        except:
            dia = 1
            mes = mes + 1
            if mes > 12:
                mes = 1
                año = año + 1

    # Día con más y menos pasajeros
    max_pasajeros = chiva.pasajeros[0]
    min_pasajeros = chiva.pasajeros[0]
    pos_max = 0
    pos_min = 0
    for i in range(1, dias):
        if chiva.pasajeros[i] > max_pasajeros:
            max_pasajeros = chiva.pasajeros[i]
            pos_max = i
        if chiva.pasajeros[i] < min_pasajeros:
            min_pasajeros = chiva.pasajeros[i]
            pos_min = i

    fecha_max = fechas[pos_max]
    fecha_min = fechas[pos_min]

    # Contadores de niveles
    cont_baja = 0
    cont_regular = 0
    cont_buena = 0
    cont_alta = 0
    for p in chiva.pasajeros:
        nivel = clasificar_nivel(p, chiva.puestos)
        if nivel == "baja":
            cont_baja = cont_baja + 1
        elif nivel == "regular":
            cont_regular = cont_regular + 1
        elif nivel == "buena":
            cont_buena = cont_buena + 1
        else:
            cont_alta = cont_alta + 1

    niveles = {
        "baja": cont_baja,
        "regular": cont_regular,
        "buena": cont_buena,
        "alta": cont_alta,
    }

    # Racha más larga de ocupación baja
    racha_longitud = 0
    racha_inicio = None
    actual = 0
    inicio_actual = None

    for i in range(dias):
        if clasificar_nivel(chiva.pasajeros[i], chiva.puestos) == "baja":
            if actual == 0:
                inicio_actual = fechas[i]
            actual = actual + 1
            if actual > racha_longitud:
                racha_longitud = actual
                racha_inicio = inicio_actual
        else:
            actual = 0
            inicio_actual = None

    # Días faltantes hasta hoy
    hoy = date.today()
    ultimo_dia = fechas[dias - 1]
    faltan = 0
    primer_faltante = None
    ultimo_faltante = None

    if ultimo_dia < hoy:
        año = ultimo_dia.year
        mes = ultimo_dia.month
        dia = ultimo_dia.day
        while True:
            dia = dia + 1
            try:
                fecha_actual = date(año, mes, dia)
            except:
                dia = 1
                mes = mes + 1
                if mes > 12:
                    mes = 1
                    año = año + 1
                fecha_actual = date(año, mes, dia)

            faltan = faltan + 1
            if primer_faltante is None:
                primer_faltante = fecha_actual
            ultimo_faltante = fecha_actual

            if fecha_actual >= hoy:
                break

    return {
        "nombre": chiva.nombre,
        "puestos": chiva.puestos,
        "dias": dias,
        "total": total,
        "promedio": round(promedio, 2),
        "porcentaje": porcentaje,
        "desviacion": desviacion,
        "fecha_max": fecha_max,
        "fecha_min": fecha_min,
        "niveles": niveles,
        "racha_longitud": racha_longitud,
        "racha_inicio": racha_inicio,
        "faltan": faltan,
        "primer_faltante": primer_faltante,
        "ultimo_faltante": ultimo_faltante,
        "ultimo_dia": ultimo_dia,
    }

def convertir_entero(texto):
    """Convierte un texto a entero. Devuelve None si no es un entero válido."""
    if texto is None:
        return None
    try:
        return int(texto)
    except (ValueError, TypeError):
        return None