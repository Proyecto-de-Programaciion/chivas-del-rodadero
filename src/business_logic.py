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


def convertir_entero(texto):
    if texto is None:
        return None
    try:
        return int(texto)
    except ValueError:
        return None


def porcentaje(chiva):
    total = 0
    for fecha, pasajeros in chiva.dias:
        total = total + pasajeros
    return (total / (len(chiva.dias) * chiva.numero_de_puestos)) * 100


def extremos_ocupacion(lista_chivas):
    ocupaciones = []                                  
    for chiva in lista_chivas:                        
        if len(chiva.dias) > 0:
            total = 0
            for fecha, pasajeros in chiva.dias:       
                total = total + pasajeros
            porcentaje_ocupacion = (total / (len(chiva.dias) * chiva.numero_de_puestos)) * 100
            ocupaciones.append([chiva, porcentaje_ocupacion]) 
    if len(ocupaciones) == 0:
        raise ValueError("Ninguna chiva tiene días registrados.")

    mejor = ocupaciones[0]
    peor = ocupaciones[0]
    for fila in ocupaciones:
        if fila[1] > mejor[1]:
            mejor = fila
        if fila[1] < peor[1]:
            peor = fila
    return mejor[0], peor[0]

def cargar_chivas(ruta, lista_chivas, nombres):
    if len(lista_chivas) > 0:
        raise RuntimeError("La carga solo se hace con el programa sin chivas.")

    archivo = open(ruta, encoding="utf-8")
    cargadas = 0
    descartadas = []
    numero = 0
    for linea in archivo:
        numero = numero + 1
        if numero > 1 and linea.strip() != "":
            try:
                campos = separar_campos(linea)
                if len(campos) != 5:
                    raise ValueError("no tiene cinco campos")

                nombre = campos[0]
                puestos = convertir_entero(campos[1])
                año = convertir_entero(campos[2])
                mes = convertir_entero(campos[3])
                dia = convertir_entero(campos[4])

                if nombre == "":
                    raise ValueError("el nombre no puede estar vacío")
                if nombre in nombres:
                    raise ValueError("ya existe una chiva con ese nombre")
                if puestos is None:
                    raise ValueError("los puestos deben ser un número entero")
                if puestos < 1:
                    raise ValueError("la chiva debe tener al menos un puesto")
                if año is None or mes is None or dia is None:
                    raise ValueError("la fecha no es válida")
                try:
                    fecha = date(año, mes, dia)
                except ValueError:
                    raise ValueError("la fecha no es válida")

                lista_chivas.append(Chiva(nombre, puestos, fecha))
                nombres.add(nombre)
                cargadas = cargadas + 1
            except ValueError as error:
                descartadas.append((numero, error))
    archivo.close()
    return cargadas, descartadas


def separar_campos(linea):
    campos = []
    actual = ""
    for letra in linea:
        if letra == ";":
            campos.append(actual.strip())
            actual = ""
        else:
            actual = actual + letra
    campos.append(actual.strip())
    return campos


def cargar_linea_pasajeros(linea, lista_chivas):
    campos = separar_campos(linea)
    if len(campos) != 2:
        raise ValueError("no tiene dos campos")

    nombre = campos[0]
    texto_pasajeros = campos[1]

    chiva = buscar_chiva(lista_chivas, nombre)
    if chiva is None:
        raise ValueError(f"no hay una chiva llamada {nombre}")

    pasajeros = convertir_entero(texto_pasajeros)
    if pasajeros is None:
        raise ValueError("los pasajeros deben ser un número entero")

    if pasajeros < 0 or pasajeros > chiva.numero_de_puestos:
        raise ValueError(f"los pasajeros van de 0 a {chiva.numero_de_puestos}")

    chiva.registrar_dia(pasajeros)


def cargar_pasajeros(ruta, lista_chivas):
    archivo = open(ruta, encoding="utf-8")
    cargados = 0
    descartadas = []
    numero = 0
    for linea in archivo:
        numero = numero + 1
        if numero > 1 and linea.strip() != "":
            try:
                cargar_linea_pasajeros(linea, lista_chivas)
                cargados = cargados + 1
            except ValueError as error:
                descartadas.append((numero, error))
    archivo.close()
    return cargados, descartadas