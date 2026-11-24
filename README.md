## ðŸŽ¬ DemostraciÃ³n

> **â–¶ Ver video final completo (editado y subtitulado):** [Haz clic aquÃ­ para abrirlo](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero/releases/download/video-final-v1/resultado_final.mp4)

| Video | DescripciÃ³n | Ver |
|---|---|---|
| ðŸŽ¥ **Resultado final** | 3 clips unidos, silencios recortados, transiciones, color, audio normalizado y subtÃ­tulos quemados | [â–¶ Abrir video](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero/releases/download/video-final-v1/resultado_final.mp4) |
| Descarga directa | Archivo MP4 alojado en GitHub Releases | [â¬‡ Descargar](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero/releases/download/video-final-v1/resultado_final.mp4) |
| Copia en el repositorio | ideos/resultado_final.mp4 | [â–¶ Ver en repo](videos/resultado_final.mp4) |

<details>
<summary>Proceso de ediciÃ³n aplicado</summary>

1. **Recorte de silencios:** pausas > 1.2 s por debajo de -35 dB (margen natural de 0.15 s).
2. **UniÃ³n:** clips 1 â†’ 2 â†’ 3 con xfade=fade:d=0.4 y crossfade=d=0.4.
3. **Imagen y audio:** 1920Ã—1080 @ 30 fps, eq=contrast=1.05:saturation=1.1, loudnorm=I=-16.
4. **SubtÃ­tulos:** transcripciÃ³n con faster-whisper (modelo ase, int8, espaÃ±ol), frases de mÃ¡ximo 8 palabras, quemados con subtitles.
5. **Render:** libx264 -preset veryfast -crf 23, AAC 192 kbps, +faststart. DuraciÃ³n: 10:59.

</details>

<div align="center">

# 🚌 Chivas del Rodadero

### Control diario de pasajeros e indicadores de ocupación

**Fundamentos de Programación · Universidad del Magdalena · 2026-II · Alternativa F**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Estado: entregado](https://img.shields.io/badge/estado-entregado-2ea44f)](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero)
[![Universidad del Magdalena](https://img.shields.io/badge/Unimagdalena-Ingeniería-0768a9)](https://www.unimagdalena.edu.co/)
[![Entrega: 23--11--2026](https://img.shields.io/badge/entrega-23--11--2026-orange)](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero)

</div>

---

## 📑 Contenido

- [🎬 Demostración](#-demostración)
- [🧭 Estructura del repositorio](#-estructura-del-repositorio)
- [🚀 Cómo ejecutarlo](#-cómo-ejecutarlo)
- [📦 Productos](#-productos)
- [👥 Equipo](#-equipo)
- [📊 Evidencia del trabajo en equipo](#-evidencia-del-trabajo-en-equipo)

---

## 🎬 Demostración

| Video | Descripción | Ver |
|---|---|---|
| Parte 1 | Recorrido general del programa y menú principal | [▶ Abrir](<videos/resultado_final.mp4 2026-11-22 at 6.09.48 PM.mp4>) |
| Parte 2 | Informes, ocupación y carga de archivos | [▶ Abrir](<videos/resultado_final.mp4 2026-11-22 at 6.29.59 PM.mp4>) |

---

## 🧭 Estructura del repositorio

``text
.
├── 📁 datos/      → CSV de prueba y 68 casos de verificación
├── 📁 docs/       → Documentos PDF y evidencia del equipo
├── 📁 src/        → Código fuente (lógica + interfaz + alternativa)
├── 📁 videos/     → Demostraciones en MP4
├── .gitignore
└── README.md
``

La lógica (src/business_logic.py) está separada de la interfaz (src/user_interface.py): no imprime ni pide datos, así que puede reutilizarse con otra interfaz.

---

## 🚀 Cómo ejecutarlo

Requiere **Python 3.10 o superior** y solo usa la biblioteca estándar.

``bash
git clone https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero.git
cd chivas-del-rodadero
python src/user_interface.py
``

<details>
<summary>Ver el menú principal</summary>

``text
1. Crear una chiva
2. Registrar los pasajeros del día siguiente
3. Simular días
4. Ver el informe de una chiva
5. Ver la chiva con el porcentaje de ocupación más alto y el más bajo
6. Cargar las chivas y los pasajeros desde archivos
7. Salir
``

</details>

---

## 📦 Productos

| Producto | Ubicación |
|---|---|
| Lógica de negocio | [src/business_logic.py](src/business_logic.py) |
| Interfaz de consola | [src/user_interface.py](src/user_interface.py) |
| Documento de análisis | [docs/Documento de Analisis.pdf](<docs/Documento de Analisis.pdf>) |
| Informe integral | [docs/Informe Integral del Trabajo.pdf](<docs/Informe Integral del Trabajo.pdf>) |
| Informe de uso de IA | [docs/Informe Uso IA Generativa.pdf](<docs/Informe Uso IA Generativa.pdf>) |
| Términos de referencia | [docs/Trabajo de fin de curso - Términos de referencia.pdf](<docs/Trabajo de fin de curso - Términos de referencia.pdf>) |
| Casos de verificación | [datos/casos_verificacion.csv](datos/casos_verificacion.csv) |
| Datos de prueba | [datos/](datos/) |
| Videos | [ideos/](videos/) |

### Niveles de ocupación

| Nivel | Porcentaje de puestos ocupados |
|---|---|
| 🔴 Baja | menos del 45 % |
| 🟡 Regular | del 45 % a menos del 70 % |
| 🟢 Buena | del 70 % a menos del 90 % |
| 🔵 Alta | 90 % o más |

---

## 👥 Equipo

| Integrante | GitHub |
|---|---|
| ![Aarón](https://github.com/AaronFernandez10.png?size=32) **Aarón Enrique Fernández Salcedo** | [@AaronFernandez10](https://github.com/AaronFernandez10) |
| ![Stephania](https://github.com/stephaniabarriosmunoz-design.png?size=32) **Stephania Michelle Barrios Muñoz** | [@stephaniabarriosmunoz-design](https://github.com/stephaniabarriosmunoz-design) |
| ![Sebastián](https://github.com/pabonsebastian106-source.png?size=32) **Sebastián David Pabón Montero** | [@pabonsebastian106-source](https://github.com/pabonsebastian106-source) |

Repositorio de la organización **[Proyecto-de-Programaciion](https://github.com/Proyecto-de-Programaciion)** · Team: [Equipo Chivas del Rodadero](https://github.com/orgs/Proyecto-de-Programaciion/teams/equipo-chivas-del-rodadero)

---

## 📊 Evidencia del trabajo en equipo

| Evidencia | Enlace |
|---|---|
| Planificación por incrementos | [6 hitos](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero/milestones) |
| Tareas asignadas | [31 issues](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero/issues) |
| Seguimiento | [Tablero de Projects](https://github.com/orgs/Proyecto-de-Programaciion/projects/1) |
| Dificultades resueltas | [Issues con etiqueta dificultad](=label%3Adificultad) |
| Detalle documentado | [docs/EVIDENCIA_EQUIPO.md](docs/EVIDENCIA_EQUIPO.md) |
| Historial de commits | [Commits](https://github.com/Proyecto-de-Programaciion/chivas-del-rodadero/commits/main) |

---

<div align="center">

Desarrollado con apoyo de herramientas de IA generativa · Universidad del Magdalena · 2026

</div>