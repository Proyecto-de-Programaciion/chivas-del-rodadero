import random
from datetime import date, timedelta

class Chiva:
    def __init__(self, nombre, numero_de_puestos, fecha_de_inicio_de_registro):
        self.nombre = nombre
        self.numero_de_puestos = numero_de_puestos
        self.fecha_de_inicio_de_registro = fecha_de_inicio_de_registro
        self.dias = []

    def fecha_siguiente(self):
        año = self.fecha_de_inicio_de_registro.year
        mes = self.fecha_de_inicio_de_registro.month
        dia = self.fecha_de_inicio_de_registro.day
        for _ in range(len(self.dias)):
            dia = dia + 1
            try:
                date(año, mes, dia)
            except ValueError:
                dia = 1
                mes = mes + 1
                if mes > 12:
                    mes = 1
                    año = año + 1
        return date(año, mes, dia)

    def registrar_dia(self, pasajeros):
        self.dias.append((self.fecha_siguiente(), pasajeros))


def validar_pasajeros(pasajeros, numero_de_puestos):
    if pasajeros < 0 or pasajeros > numero_de_puestos:
        return f"Error: los pasajeros van de 0 a {numero_de_puestos}."
    return None


def crear_chiva(lista_chivas, nombres, nombre, puestos, año, mes, dia):
    nombre = nombre.strip()
    if nombre == "":
        return "Error: el nombre no puede estar vacío."
    if nombre in nombres:
        return "Error: ya existe una chiva con ese nombre."
    if puestos is None:
        return "Error: los puestos deben ser un número entero."
    if puestos < 1:
        return "Error: la chiva debe tener al menos un puesto."
    if año is None or mes is None or dia is None:
        return "Error: la fecha no es válida."
    try:
        fecha = date(año, mes, dia)
    except ValueError:
        return "Error: la fecha no es válida."

    lista_chivas.append(Chiva(nombre, puestos, fecha))
    nombres.add(nombre)
    return None


def buscar_chiva(lista_chivas, nombre):
    nombre = nombre.strip()
    for chiva in lista_chivas:
        if chiva.nombre == nombre:
            return chiva
    return None


def validar_simulacion(dias, minimo, maximo, numero_de_puestos):
    if dias is None:
        return "Error: el número de días debe ser un entero."
    if dias < 1:
        return "Error: se debe simular al menos un día."
    if minimo is None:
        return "Error: los pasajeros deben ser un número entero."
    if minimo < 0 or minimo > numero_de_puestos:
        return f"Error: los pasajeros van de 0 a {numero_de_puestos}."
    if maximo is None:
        return "Error: los pasajeros deben ser un número entero."
    if maximo < 0 or maximo > numero_de_puestos:
        return f"Error: los pasajeros van de 0 a {numero_de_puestos}."
    if minimo > maximo:
        return "Error: el mínimo no puede ser mayor que el máximo."
    return None


def simular_dias(chiva, dias, minimo, maximo):
    error = validar_simulacion(dias, minimo, maximo, chiva.numero_de_puestos)
    if error is not None:
        return error
    for _ in range(dias):
        chiva.registrar_dia(random.randint(minimo, maximo))
    return None


# ---------- Punto 6 ----------
def dia_mayor_y_menor(chiva):
    fecha_max, max_pasajeros = chiva.dias[0]
    fecha_min, min_pasajeros = chiva.dias[0]
    for fecha, pasajeros in chiva.dias:
        if pasajeros > max_pasajeros:
            max_pasajeros = pasajeros
            fecha_max = fecha
        if pasajeros < min_pasajeros:
            min_pasajeros = pasajeros
            fecha_min = fecha
    return fecha_max, fecha_min


# ---------- Punto 7 ----------
def nivel_de_ocupacion(pasajeros, numero_de_puestos):
    if pasajeros * 100 < 45 * numero_de_puestos:
        return "baja"
    if pasajeros * 100 < 70 * numero_de_puestos:
        return "regular"
    if pasajeros * 100 < 90 * numero_de_puestos:
        return "buena"
    return "alta"


def contar_niveles(chiva):
    conteo = {"baja": 0, "regular": 0, "buena": 0, "alta": 0}
    for fecha, pasajeros in chiva.dias:
        nivel = nivel_de_ocupacion(pasajeros, chiva.numero_de_puestos)
        conteo[nivel] = conteo[nivel] + 1
    return conteo


# ---------- Punto 8 ----------
def racha_mas_larga_baja(chiva):
    mejor_longitud = 0
    mejor_inicio = None
    longitud_actual = 0
    inicio_actual = None
    for fecha, pasajeros in chiva.dias:
        if nivel_de_ocupacion(pasajeros, chiva.numero_de_puestos) == "baja":
            if longitud_actual == 0:
                inicio_actual = fecha
            longitud_actual = longitud_actual + 1
            if longitud_actual > mejor_longitud:
                mejor_longitud = longitud_actual
                mejor_inicio = inicio_actual
        else:
            longitud_actual = 0
            inicio_actual = None
    return mejor_longitud, mejor_inicio


# ---------- Punto 9 ----------
def dias_sin_registrar(chiva):
    ultimo_dia = chiva.dias[-1][0]
    hoy = date.today()
    ayer = hoy - timedelta(days=1)
    faltan = (ayer - ultimo_dia).days
    if faltan < 0:
        faltan = 0
    return ultimo_dia, faltan, ultimo_dia + timedelta(days=1), ayer


def generar_informe(chiva):
    if len(chiva.dias) == 0:
        return f"La chiva {chiva.nombre} no tiene días registrados."

    total_pasajeros = 0
    for fecha, pasajeros in chiva.dias:
        total_pasajeros = total_pasajeros + pasajeros

    dias_registrados = len(chiva.dias)
    promedio = total_pasajeros / dias_registrados
    porcentaje = promedio / chiva.numero_de_puestos * 100

    suma_cuadrados = 0
    for fecha, pasajeros in chiva.dias:
        diferencia = pasajeros - promedio
        suma_cuadrados = suma_cuadrados + diferencia * diferencia
    desviacion = (suma_cuadrados / dias_registrados) ** 0.5

    fecha_max, fecha_min = dia_mayor_y_menor(chiva)

    niveles = contar_niveles(chiva)

    longitud, inicio = racha_mas_larga_baja(chiva)
    if longitud == 0:
        linea_racha = "Racha más larga en ocupación baja: la chiva no tuvo ningún día en ocupación baja"
    else:
        linea_racha = (
            f"Racha más larga en ocupación baja: {longitud} días, "
            f"empezó el {inicio}"
        )

    ultimo_dia, faltan, primero_faltante, ultimo_faltante = dias_sin_registrar(chiva)
    if faltan == 0:
        linea_registro = "Estado del registro: el registro está al día"
    else:
        linea_registro = (
            f"Días por registrar: {faltan}, del {primero_faltante} "
            f"al {ultimo_faltante}"
        )

    informe = (
        f"Chiva: {chiva.nombre}\n"
        f"Puestos: {chiva.numero_de_puestos}\n"
        f"Días registrados: {dias_registrados}\n"
        f"Pasajeros totales: {total_pasajeros}\n"
        f"Promedio de pasajeros por día: {round(promedio, 2)}\n"
        f"Porcentaje de ocupación: {round(porcentaje, 2)}%\n"
        f"Desviación estándar: {round(desviacion, 2)}\n"
        f"Día con más pasajeros: {fecha_max}\n"
        f"Día con menos pasajeros: {fecha_min}\n"
        f"Días en ocupación baja: {niveles['baja']}\n"
        f"Días en ocupación regular: {niveles['regular']}\n"
        f"Días en ocupación buena: {niveles['buena']}\n"
        f"Días en ocupación alta: {niveles['alta']}\n"
        f"{linea_racha}\n"
        f"Último día registrado: {ultimo_dia}\n"
        f"{linea_registro}"
    )
    return informe
