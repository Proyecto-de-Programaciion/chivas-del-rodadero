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
    fecha_mayor, pasajeros_mayor = chiva.dias[0]
    fecha_menor, pasajeros_menor = chiva.dias[0]
 
    for fecha, pasajeros in chiva.dias:
        if pasajeros > pasajeros_mayor:
            fecha_mayor = fecha
            pasajeros_mayor = pasajeros
 
        if pasajeros < pasajeros_menor:
            fecha_menor = fecha
            pasajeros_menor = pasajeros
    baja = 0
    regular = 0
    buena = 0
    alta = 0

    for fecha, pasajeros in chiva.dias:
        ocupacion = pasajeros / chiva.numero_de_puestos * 100
 
        if ocupacion < 45:
            baja = baja + 1
        elif ocupacion < 70:
            regular = regular + 1
        elif ocupacion < 90:
            buena = buena + 1
        else:
            alta = alta + 1

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