import random
from datetime import date

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


def generar_informe(chiva):
    dias = len(chiva.dias)

    if dias == 0:
        return {
            "nombre": chiva.nombre,
            "puestos": chiva.numero_de_puestos,
            "dias": 0,
        }

    fechas = []
    pasajeros = []
    for fecha, p in chiva.dias:
        fechas.append(fecha)
        pasajeros.append(p)

    total = 0
    for p in pasajeros:
        total = total + p

    promedio = total / dias
    porcentaje = round((promedio / chiva.numero_de_puestos) * 100, 2)

    suma_cuadrados = 0
    for p in pasajeros:
        diferencia = p - promedio
        suma_cuadrados = suma_cuadrados + diferencia * diferencia
    desviacion = round((suma_cuadrados / dias) ** 0.5, 2)

    max_pasajeros = pasajeros[0]
    min_pasajeros = pasajeros[0]
    pos_max = 0
    pos_min = 0
    for i in range(1, dias):
        if pasajeros[i] > max_pasajeros:
            max_pasajeros = pasajeros[i]
            pos_max = i
        if pasajeros[i] < min_pasajeros:
            min_pasajeros = pasajeros[i]
            pos_min = i

    fecha_max = fechas[pos_max]
    fecha_min = fechas[pos_min]

    cont_baja = 0
    cont_regular = 0
    cont_buena = 0
    cont_alta = 0
    for p in pasajeros:
        nivel = clasificar_nivel(p, chiva.numero_de_puestos)
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

    racha_longitud = 0
    racha_inicio = None
    actual = 0
    inicio_actual = None

    for i in range(dias):
        if clasificar_nivel(pasajeros[i], chiva.numero_de_puestos) == "baja":
            if actual == 0:
                inicio_actual = fechas[i]
            actual = actual + 1
            if actual > racha_longitud:
                racha_longitud = actual
                racha_inicio = inicio_actual
        else:
            actual = 0
            inicio_actual = None

    hoy = date.today()
    ultimo_dia = fechas[dias - 1]
    faltan = 0
    primer_faltante = None
    ultimo_faltante = None

    siguiente = ultimo_dia
    while True:
        año = siguiente.year
        mes = siguiente.month
        dia = siguiente.day + 1
        try:
            candidato = date(año, mes, dia)
        except ValueError:
            dia = 1
            mes = mes + 1
            if mes > 12:
                mes = 1
                año = año + 1
            candidato = date(año, mes, dia)

        if candidato >= hoy:
            break

        faltan = faltan + 1
        if primer_faltante is None:
            primer_faltante = candidato
        ultimo_faltante = candidato
        siguiente = candidato

    return {
        "nombre": chiva.nombre,
        "puestos": chiva.numero_de_puestos,
        "dias": dias,
        "total": total,
        "promedio": round(promedio, 2),
        "porcentaje": porcentaje,
        "desviacion": round(desviacion, 2),
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

    informe = (
        f"Chiva: {chiva.nombre}\n"
        f"Puestos: {chiva.numero_de_puestos}\n"
        f"Días registrados: {dias_registrados}\n"
        f"Pasajeros totales: {total_pasajeros}\n"
        f"Promedio de pasajeros por día: {round(promedio, 2)}\n"
        f"Porcentaje de ocupación: {round(porcentaje, 2)}%\n"
        f"Desviación estándar: {round(desviacion, 2)}\n"
        f"Día de más pasajeros: {fecha_mayor}\n"
        f"Día de menos pasajeros: {fecha_menor}\n"
        f"Días en ocupación baja: {baja}\n"
        f"Días en ocupación regular: {regular}\n"
        f"Días en ocupación buena: {buena}\n"        
        f"Días en ocupación alta: {alta}\n"
    )
    return informe