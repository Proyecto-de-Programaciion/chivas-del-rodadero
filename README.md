Chivas del Rodadero: control de ocupación de pasajeros

Programa en Python para llevar el registro diario de pasajeros de las chivas turísticas de la empresa **Chivas del Rodadero** (Santa Marta y El Rodadero) y calcular los indicadores con que la empresa vigila la ocupación de cada chiva.

Trabajo de fin de curso de **Fundamentos de Programación**, Facultad de Ingeniería, Universidad del Magdalena. Alternativa F.

---

## 📖 Contexto

Cada chiva (la Parrandera, la Cumbiamba, la Guacherna, la Puya...) tiene un nombre, un número fijo de puestos y hace un solo recorrido nocturno al día. Su registro empieza en una fecha de inicio y avanza un día tras otro, sin saltarse ninguno. Al terminar cada recorrido, el conductor entrega el conteo de pasajeros y ese dato se agrega al registro.

Con esos registros, el programa responde preguntas como:

- ¿Cuál es el promedio de pasajeros por día y el porcentaje de ocupación de cada chiva?
- ¿Cuánto varía la cantidad de pasajeros de un día a otro?
- ¿Cuántos días estuvo cada chiva en ocupación baja, regular, buena o alta?
- ¿Cuál fue la racha más larga de días seguidos con ocupación baja? (señal de que conviene cambiar el recorrido o el horario)
- ¿Cuántos días faltan por registrar?
- ¿Qué chiva tiene la mejor y la peor ocupación de la flota?

## ✨ Funcionalidades

| # | Funcionalidad | Descripción |
|---|---|---|
| 1 | Crear una chiva | Nombre, puestos y fecha de inicio, con validaciones en orden |
| 2 | Registrar el día siguiente | Muestra la fecha que sigue y lee los pasajeros hasta que sean válidos |
| 3 | Simular días | Agrega días con pasajeros al azar entre un mínimo y un máximo |
| 4 | Informe de una chiva | Días registrados, pasajeros totales, promedio y porcentaje de ocupación |
| 5 | Desviación estándar | Variación de los pasajeros entre días |
| 6 | Día de más y de menos pasajeros | En caso de empate, el primero |
| 7 | Días por nivel de ocupación | Conteo en baja, regular, buena y alta |
| 8 | Racha más larga en ocupación baja | Longitud y fecha de inicio |
| 9 | Días sin registrar | Compara con la fecha actual del computador |
| 10 | Varias chivas en el mismo programa | Búsqueda por nombre, sensible a mayúsculas y tildes |
| 11 | Ocupación más alta y más baja | Compara todas las chivas con días registrados |
| 12 | Cargar chivas desde CSV | Descarta las líneas inválidas informando número y causa |
| 13 | Cargar pasajeros desde CSV | Igual que el anterior, día a día por chiva |
| 14 | Menú de consola | Siete opciones numeradas |

### Niveles de ocupación

Se calculan con el porcentaje de puestos ocupados en cada día:

| Nivel | Porcentaje de puestos ocupados |
|---|---|
| Baja | menos del 45 % |
| Regular | del 45 % a menos del 70 % |
| Buena | del 70 % a menos del 90 % |
| Alta | 90 % o más |

### Fórmulas

- **Pasajeros totales** = suma de los pasajeros de todos los días registrados
- **Promedio** = pasajeros totales / días registrados
- **Porcentaje de ocupación** = (promedio / puestos) × 100
- **Desviación estándar** = √( Σ(pasajeros del día − promedio)² / días registrados )

Los valores del informe se redondean a dos decimales con `round`.

## 🗂️ Estructura del repositorio

```
.
├── business_logic.py        # Lógica del negocio (independiente de la interfaz)
├── user_interface.py        # Interfaz de consola con el menú
├── datos/                   # Archivos CSV de chivas y pasajeros
├── verificacion/            # Casos de verificación con datos y salida esperada
├── docs/
│   ├── analisis.md          # Documento de análisis de requisitos
│   ├── informe_integral.md  # Informe de los incrementos de desarrollo
│   └── informe_uso_ia.md    # Informe del uso de IA generativa, con evidencias
└── README.md
```

La lógica del negocio está separada de la interfaz: `business_logic.py` no depende de cómo el usuario interactúe con el programa.

## ▶️ Cómo ejecutarlo

Requiere **Python 3.10 o superior** y solo usa la biblioteca estándar.

```bash
git clone <https://github.com/stephaniabarriosmunoz-design/chivas-del-rodadero>
cd <nombre-del-repositorio>
python user_interface.py
```

### Menú principal

```
1. Crear una chiva
2. Registrar los pasajeros del día siguiente
3. Simular días
4. Ver el informe de una chiva
5. Ver la chiva con el porcentaje de ocupación más alto y el más bajo
6. Cargar las chivas y los pasajeros desde archivos
7. Salir
```

### Formato de los archivos CSV

Codificación UTF-8, campos separados por punto y coma, con encabezado en la primera línea.

`chivas.csv`

```
chiva;puestos;año;mes;día
Parrandera;40;2026;11;1
Cumbiamba;30;2026;11;1
```

`pasajeros.csv`

```
chiva;pasajeros
Parrandera;36
Cumbiamba;12
```

Los espacios alrededor de los campos se ignoran, las líneas vacías se saltan y las líneas con errores se descartan mostrando su número y la causa. La carga desde archivos solo se permite cuando el programa todavía no tiene chivas.

## ✅ Verificación

Cada caso de verificación tiene sus datos de entrada, sus archivos y su salida esperada, y se comprueba ejecutando `user_interface.py`. Los casos cubren todos los caminos de ejecución y todas las validaciones de cada requisito. Se encuentran en la carpeta `verificacion/`.

## 👥 Equipo

| Integrante | GitHub |
| Aaron Fernandez | [@AaronFernandez10](https://github.com/usuario1) |
| Stephania Barrios| [@stephaniabarriosmunoz-design](https://github.com/stephaniabarriosmunoz-design) |
| Sebastian Pabon | [@pabonsebastian106-source](https://github.com/pabonsebastian106-source) |

## 🧑‍🏫 Información académica

- **Universidad:** Universidad del Magdalena, Facultad de Ingeniería
- **Curso:** Fundamentos de Programación
- **Programa:** Ingeniería en Ciencia de Datos
- **Período:** 2026-II

Este proyecto se desarrolló con apoyo de herramientas de IA generativa.
