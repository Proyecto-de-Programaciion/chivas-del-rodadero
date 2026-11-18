import customtkinter as ctk

from logica import (
    buscar_chiva,
    crear_chiva,
    simular_dias,
    validar_pasajeros,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

FONDO = "#1b2631"
PANEL = "#273746"
ACENTO = "#f39c12"
ACENTO_HOVER = "#e67e22"
TEXTO = "#ecf0f1"
EXITO = "#2ecc71"
ERROR = "#e74c3c"

FUENTE_TITULO = ("Segoe UI", 26, "bold")
FUENTE_TEXTO = ("Segoe UI", 14)
FUENTE_NEGRITA = ("Segoe UI", 14, "bold")
SIN_CHIVAS = "Sin chivas"


def leer_entero(texto):
    try:
        return int(texto.strip())
    except ValueError:
        return None


def formato_fecha(fecha):
    return f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year}"


class VentanaChivas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Registro de chivas")
        self.geometry("780x620")
        self.minsize(700, 560)
        self.configure(fg_color=FONDO)

        self.lista_chivas = []
        self.nombres = set()
        self.selectores = []

        self._encabezado()
        self._mensaje()
        self._pestanas()

        # Chiva de ejemplo para practicar
        crear_chiva(self.lista_chivas, self.nombres, "La Azul", 10, 2026, 1, 5)
        self.actualizar_listas()

    # ---------- Estructura ----------

    def _encabezado(self):
        ctk.CTkLabel(
            self,
            text="Registro de chivas",
            font=FUENTE_TITULO,
            text_color=ACENTO,
        ).pack(pady=(25, 5))

    def _mensaje(self):
        self.lbl_mensaje = ctk.CTkLabel(self, text="", font=FUENTE_NEGRITA)
        self.lbl_mensaje.pack(side="bottom", pady=12)

    def _pestanas(self):
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=PANEL,
            segmented_button_fg_color=FONDO,
            segmented_button_selected_color=ACENTO,
            segmented_button_selected_hover_color=ACENTO_HOVER,
            segmented_button_unselected_color=FONDO,
            text_color=TEXTO,
        )
        self.tabview.pack(fill="both", expand=True, padx=25, pady=(10, 0))

        self._tab_crear(self.tabview.add("Crear chiva"))
        self._tab_registrar(self.tabview.add("Registrar día"))
        self._tab_simular(self.tabview.add("Simular días"))
        self._tab_ver(self.tabview.add("Ver registro"))

    # ---------- Widgets reutilizables ----------

    def _formulario(self, padre):
        marco = ctk.CTkFrame(padre, fg_color="transparent")
        marco.pack(fill="x", padx=30, pady=20)
        marco.columnconfigure(1, weight=1)
        return marco

    def _campo(self, padre, etiqueta, fila):
        ctk.CTkLabel(padre, text=etiqueta, font=FUENTE_TEXTO).grid(
            row=fila, column=0, sticky="w", pady=10, padx=(0, 20)
        )
        entrada = ctk.CTkEntry(
            padre,
            font=FUENTE_TEXTO,
            height=38,
            corner_radius=10,
            fg_color=FONDO,
            border_color=ACENTO,
        )
        entrada.grid(row=fila, column=1, sticky="ew", pady=10)
        return entrada

    def _selector(self, padre, fila):
        ctk.CTkLabel(padre, text="Chiva:", font=FUENTE_TEXTO).grid(
            row=fila, column=0, sticky="w", pady=10, padx=(0, 20)
        )
        selector = ctk.CTkOptionMenu(
            padre,
            values=[SIN_CHIVAS],
            font=FUENTE_TEXTO,
            height=38,
            corner_radius=10,
            fg_color=ACENTO,
            button_color=ACENTO_HOVER,
            button_hover_color="#d35400",
            text_color=FONDO,
            dropdown_fg_color=PANEL,
            dropdown_text_color=TEXTO,
        )
        selector.grid(row=fila, column=1, sticky="ew", pady=10)
        self.selectores.append(selector)
        return selector

    def _boton(self, padre, texto, comando):
        return ctk.CTkButton(
            padre,
            text=texto,
            command=comando,
            font=FUENTE_NEGRITA,
            height=42,
            corner_radius=12,
            fg_color=ACENTO,
            hover_color=ACENTO_HOVER,
            text_color=FONDO,
        )

    def mostrar(self, texto, ok=False):
        self.lbl_mensaje.configure(text=texto, text_color=EXITO if ok else ERROR)

    def actualizar_listas(self):
        nombres = [chiva.nombre for chiva in self.lista_chivas] or [SIN_CHIVAS]
        for selector in self.selectores:
            actual = selector.get()
            selector.configure(values=nombres)
            if actual not in nombres:
                selector.set(nombres[0])

    def _chiva_de(self, selector):
        return buscar_chiva(self.lista_chivas, selector.get())

    # ---------- Pestaña 1: crear ----------

    def _tab_crear(self, padre):
        marco = self._formulario(padre)
        self.ent_nombre = self._campo(marco, "Nombre de la chiva:", 0)
        self.ent_puestos = self._campo(marco, "Número de puestos:", 1)
        self.ent_anio = self._campo(marco, "Año de inicio:", 2)
        self.ent_mes = self._campo(marco, "Mes de inicio:", 3)
        self.ent_dia = self._campo(marco, "Día de inicio:", 4)
        self._boton(marco, "Crear chiva", self.crear).grid(
            row=5, column=0, columnspan=2, pady=25, sticky="ew", padx=120
        )

    def crear(self):
        error = crear_chiva(
            self.lista_chivas,
            self.nombres,
            self.ent_nombre.get(),
            leer_entero(self.ent_puestos.get()),
            leer_entero(self.ent_anio.get()),
            leer_entero(self.ent_mes.get()),
            leer_entero(self.ent_dia.get()),
        )
        if error is not None:
            self.mostrar(error)
            return

        self.mostrar(f"Chiva creada: {self.ent_nombre.get().strip()}", ok=True)
        for entrada in (self.ent_nombre, self.ent_puestos, self.ent_anio,
                        self.ent_mes, self.ent_dia):
            entrada.delete(0, "end")
        self.actualizar_listas()

    # ---------- Pestaña 2: registrar un día ----------

    def _tab_registrar(self, padre):
        marco = self._formulario(padre)
        self.sel_reg = self._selector(marco, 0)
        self.sel_reg.configure(command=lambda _: self.actualizar_fecha())

        self.lbl_fecha = ctk.CTkLabel(
            marco, text="Día siguiente: —", font=FUENTE_NEGRITA, text_color=ACENTO
        )
        self.lbl_fecha.grid(row=1, column=0, columnspan=2, sticky="w", pady=15)

        self.ent_pasajeros = self._campo(marco, "Pasajeros:", 2)
        self._boton(marco, "Registrar día", self.registrar).grid(
            row=3, column=0, columnspan=2, pady=25, sticky="ew", padx=120
        )

    def actualizar_fecha(self):
        chiva = self._chiva_de(self.sel_reg)
        if chiva is None:
            self.lbl_fecha.configure(text="Día siguiente: —")
        else:
            siguiente = formato_fecha(chiva.fecha_siguiente())
            self.lbl_fecha.configure(text=f"Día siguiente: {siguiente}")

    def registrar(self):
        chiva = self._chiva_de(self.sel_reg)
        if chiva is None:
            self.mostrar("Selecciona una chiva.")
            return

        pasajeros = leer_entero(self.ent_pasajeros.get())
        if pasajeros is None:
            self.mostrar("Error: los pasajeros deben ser un número entero.")
            return

        error = validar_pasajeros(pasajeros, chiva.numero_de_puestos)
        if error is not None:
            self.mostrar(error)
            return

        chiva.registrar_dia(pasajeros)
        self.ent_pasajeros.delete(0, "end")
        self.actualizar_fecha()
        self.actualizar_tabla()
        self.mostrar("Día registrado.", ok=True)

    # ---------- Pestaña 3: simular ----------

    def _tab_simular(self, padre):
        marco = self._formulario(padre)
        self.sel_sim = self._selector(marco, 0)
        self.ent_dias = self._campo(marco, "Número de días:", 1)
        self.ent_minimo = self._campo(marco, "Pasajeros mínimos:", 2)
        self.ent_maximo = self._campo(marco, "Pasajeros máximos:", 3)
        self._boton(marco, "Simular", self.simular).grid(
            row=4, column=0, columnspan=2, pady=25, sticky="ew", padx=120
        )

    def simular(self):
        chiva = self._chiva_de(self.sel_sim)
        if chiva is None:
            self.mostrar("Selecciona una chiva.")
            return

        error = simular_dias(
            chiva,
            leer_entero(self.ent_dias.get()),
            leer_entero(self.ent_minimo.get()),
            leer_entero(self.ent_maximo.get()),
        )
        if error is not None:
            self.mostrar(error)
            return

        self.actualizar_tabla()
        self.mostrar(f"Días simulados para {chiva.nombre}.", ok=True)

    # ---------- Pestaña 4: ver registro ----------

    def _tab_ver(self, padre):
        marco = self._formulario(padre)
        self.sel_ver = self._selector(marco, 0)
        self.sel_ver.configure(command=lambda _: self.actualizar_tabla())

        self.tabla = ctk.CTkTextbox(
            padre,
            font=("Consolas", 14),
            corner_radius=12,
            fg_color=FONDO,
            text_color=TEXTO,
        )
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.actualizar_tabla()

    def actualizar_tabla(self):
        chiva = self._chiva_de(self.sel_ver)
        self.tabla.configure(state="normal")
        self.tabla.delete("1.0", "end")
        if chiva is None:
            self.tabla.insert("end", "Sin datos.")
        else:
            self.tabla.insert("end", f"{'Fecha':<16}{'Pasajeros':>10}\n")
            self.tabla.insert("end", "-" * 26 + "\n")
            for fecha, pasajeros in chiva.dias:
                self.tabla.insert("end", f"{formato_fecha(fecha):<16}{pasajeros:>10}\n")
        self.tabla.configure(state="disabled")


if __name__ == "__main__":
    VentanaChivas().mainloop()