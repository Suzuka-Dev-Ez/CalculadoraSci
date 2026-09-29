
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class CalculadoraGrafica:
    def __init__(self, root):
        self.root = root

        # -----------------------------
        # Configuración de la ventana
        # -----------------------------
        self.root.title("Calculadora Científica y Graficadora")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)

        # Resultado anterior
        self.ans = 0

        # Configuración del grid principal
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        self._crear_panel_calculadora()
        self._crear_panel_grafico()

    # ==========================================================
    # PANEL DE CALCULADORA
    # ==========================================================

    def _crear_panel_calculadora(self):
        frame_calc = ttk.LabelFrame(
            self.root,
            text="Calculadora",
            padding="10"
        )

        frame_calc.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # -----------------------------
        # Pantalla
        # -----------------------------
        self.expresion_var = tk.StringVar()

        pantalla = ttk.Entry(
            frame_calc,
            textvariable=self.expresion_var,
            font=("Consolas", 18),
            justify="right"
        )

        pantalla.grid(
            row=0,
            column=0,
            columnspan=5,
            sticky="ew",
            ipady=10,
            pady=(0, 10)
        )

        # Permitir usar el teclado
        pantalla.focus()

        # -----------------------------
        # Botones
        # -----------------------------
        botones = [
            ("C", 1, 0),
            ("⌫", 1, 1),
            ("(", 1, 2),
            (")", 1, 3),
            ("/", 1, 4),

            ("sin", 2, 0),
            ("cos", 2, 1),
            ("tan", 2, 2),
            ("sqrt", 2, 3),
            ("*", 2, 4),

            ("7", 3, 0),
            ("8", 3, 1),
            ("9", 3, 2),
            ("^", 3, 3),
            ("-", 3, 4),

            ("4", 4, 0),
            ("5", 4, 1),
            ("6", 4, 2),
            ("x²", 4, 3),
            ("+", 4, 4),

            ("1", 5, 0),
            ("2", 5, 1),
            ("3", 5, 2),
            ("%", 5, 3),
            ("=", 5, 4),

            ("0", 6, 0),
            (".", 6, 1),
            ("pi", 6, 2),
            ("e", 6, 3),
            ("Ans", 6, 4),

            ("ln", 7, 0),
            ("log", 7, 1),
            ("1/x", 7, 2),
            ("exp", 7, 3),
            ("x", 7, 4),
        ]

        # Configuración de filas y columnas
        for columna in range(5):
            frame_calc.columnconfigure(columna, weight=1)

        for fila in range(8):
            frame_calc.rowconfigure(fila, weight=1)

        # Crear botones
        for texto, fila, columna in botones:

            boton = ttk.Button(
                frame_calc,
                text=texto,
                command=lambda t=texto: self._al_pulsar_boton(t)
            )

            boton.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=2,
                pady=2
            )

    # ==========================================================
    # BOTONES DE LA CALCULADORA
    # ==========================================================

    def _al_pulsar_boton(self, texto):

        expresion = self.expresion_var.get()

        # -----------------------------
        # Limpiar
        # -----------------------------
        if texto == "C":
            self.expresion_var.set("")

        # -----------------------------
        # Borrar último carácter
        # -----------------------------
        elif texto == "⌫":
            self.expresion_var.set(expresion[:-1])

        # -----------------------------
        # Igual
        # -----------------------------
        elif texto == "=":
            self._evaluar_expresion()

        # -----------------------------
        # Funciones
        # -----------------------------
        elif texto in ("sin", "cos", "tan", "sqrt", "log", "ln", "exp"):
            self.expresion_var.set(
                expresion + f"{texto}("
            )

        # -----------------------------
        # Potencia
        # -----------------------------
        elif texto == "^":
            self.expresion_var.set(
                expresion + "**"
            )

        # -----------------------------
        # Cuadrado
        # -----------------------------
        elif texto == "x²":
            self.expresion_var.set(
                f"({expresion})**2"
            )

        # -----------------------------
        # Inverso
        # -----------------------------
        elif texto == "1/x":
            self.expresion_var.set(
                f"1/({expresion})"
            )

        # -----------------------------
        # Porcentaje
        # -----------------------------
        elif texto == "%":
            self.expresion_var.set(
                expresion + "/100"
            )

        # -----------------------------
        # Resultado anterior
        # -----------------------------
        elif texto == "Ans":
            self.expresion_var.set(
                expresion + "ans"
            )

        # -----------------------------
        # Resto de botones
        # -----------------------------
        else:
            self.expresion_var.set(
                expresion + texto
            )

    # ==========================================================
    # EVALUAR EXPRESIÓN
    # ==========================================================

    def _evaluar_expresion(self):

        expr = self.expresion_var.get()

        if not expr.strip():
            return

        contexto = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "ans": self.ans
        }

        try:

            resultado = eval(
                expr,
                {"__builtins__": None},
                contexto
            )

            # Evitar resultados extraños
            if isinstance(resultado, (int, float)):

                if not math.isfinite(resultado):
                    raise ValueError("El resultado no es finito.")

                self.ans = resultado

            self.expresion_var.set(str(resultado))

        except ZeroDivisionError:
            messagebox.showerror(
                "Error",
                "No se puede dividir entre cero."
            )

        except ValueError as error:
            messagebox.showerror(
                "Error matemático",
                f"No se pudo realizar la operación.\n\n{error}"
            )

        except Exception:
            messagebox.showerror(
                "Error",
                "La expresión matemática no es válida."
            )

    # ==========================================================
    # PANEL DE GRÁFICOS
    # ==========================================================

    def _crear_panel_grafico(self):

        frame_grafico = ttk.LabelFrame(
            self.root,
            text="Graficadora",
            padding="10"
        )

        frame_grafico.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 10),
            pady=10
        )

        frame_grafico.columnconfigure(0, weight=1)
        frame_grafico.rowconfigure(1, weight=1)

        # -----------------------------
        # Controles
        # -----------------------------

        frame_controles = ttk.Frame(frame_grafico)

        frame_controles.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        frame_controles.columnconfigure(1, weight=1)

        ttk.Label(
            frame_controles,
            text="f(x) ="
        ).grid(
            row=0,
            column=0,
            padx=(0, 5)
        )

        self.entry_fx = ttk.Entry(
            frame_controles,
            font=("Consolas", 12)
        )

        self.entry_fx.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        self.entry_fx.insert(
            0,
            "sin(x)"
        )

        # Botón graficar
        ttk.Button(
            frame_controles,
            text="Graficar",
            command=self.graficar
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        # -----------------------------
        # Rango X
        # -----------------------------

        ttk.Label(
            frame_controles,
            text="X min:"
        ).grid(
            row=1,
            column=0,
            pady=(10, 0)
        )

        self.entry_xmin = ttk.Entry(
            frame_controles,
            width=8
        )

        self.entry_xmin.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(10, 0)
        )

        self.entry_xmin.insert(
            0,
            "-10"
        )

        ttk.Label(
            frame_controles,
            text="X max:"
        ).grid(
            row=1,
            column=1,
            sticky="e",
            pady=(10, 0),
            padx=(0, 80)
        )

        self.entry_xmax = ttk.Entry(
            frame_controles,
            width=8
        )

        self.entry_xmax.grid(
            row=1,
            column=2,
            pady=(10, 0)
        )

        self.entry_xmax.insert(
            0,
            "10"
        )

        # -----------------------------
        # Matplotlib
        # -----------------------------

        self.fig, self.ax = plt.subplots(
            figsize=(6, 5),
            dpi=100
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=frame_grafico
        )

        self.canvas.get_tk_widget().grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # Graficar función inicial
        self.graficar()

    # ==========================================================
    # GRAFICAR
    # ==========================================================

    def graficar(self):

        expr = self.entry_fx.get().strip()

        if not expr:
            messagebox.showwarning(
                "Advertencia",
                "Escribe una función para graficar."
            )
            return

        try:

            # Obtener rango
            xmin = float(
                self.entry_xmin.get()
            )

            xmax = float(
                self.entry_xmax.get()
            )

            if xmin >= xmax:
                raise ValueError(
                    "X min debe ser menor que X max."
                )

            # Crear valores X
            x = np.linspace(
                xmin,
                xmax,
                2000
            )

            # Reemplazar ^ por **
            expr_np = expr.replace(
                "^",
                "**"
            )

            # Funciones permitidas
            contexto = {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "sqrt": np.sqrt,
                "log": np.log10,
                "ln": np.log,
                "exp": np.exp,
                "pi": np.pi,
                "e": np.e,
                "abs": np.abs
            }

            # Evaluar función
            y = eval(
                expr_np,
                {"__builtins__": None},
                contexto
            )

            # -----------------------------
            # Limpiar gráfico
            # -----------------------------

            self.ax.clear()

            # -----------------------------
            # Evitar líneas gigantes
            # en discontinuidades
            # -----------------------------

            y = np.asarray(y, dtype=float)

            y[~np.isfinite(y)] = np.nan

            # Valores demasiado grandes
            y[np.abs(y) > 1e4] = np.nan

            # -----------------------------
            # Dibujar
            # -----------------------------

            self.ax.plot(
                x,
                y,
                label=f"f(x) = {expr}",
                linewidth=2
            )

            # Eje X
            self.ax.axhline(
                0,
                linewidth=0.8,
                linestyle="--"
            )

            # Eje Y
            self.ax.axvline(
                0,
                linewidth=0.8,
                linestyle="--"
            )

            # Grid
            self.ax.grid(
                True,
                linestyle=":",
                alpha=0.6
            )

            # Título
            self.ax.set_title(
                "Gráfico de la función"
            )

            # Etiquetas
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")

            # Leyenda
            self.ax.legend(
                loc="upper right"
            )

            # Ajustar
            self.fig.tight_layout()

            # Actualizar
            self.canvas.draw()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error al graficar",
                f"No se pudo evaluar la función.\n\n{error}"
            )


# ==============================================================
# PROGRAMA PRINCIPAL
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalculadoraGrafica(root)

    root.mainloop()