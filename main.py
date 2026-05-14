import flet as ft
import requests


def main(page: ft.Page):

    # =====================================================
    # CONFIGURACION PAGINA
    # =====================================================

    page.title = "Metodos Numericos"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "auto"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = "#0f172a"
    page.padding = 20

    # =====================================================
    # ESTILO INPUTS
    # =====================================================

    ESTILO_INPUT = {
        "border_radius": 15,
        "filled": True,
        "bgcolor": "#1e293b",
        "border_color": "#38bdf8",
        "color": "white",
        "label_style": ft.TextStyle(color="white")
    }

    # =====================================================
    # TITULOS
    # =====================================================

    titulo = ft.Text(
        "Calculadora de Metodos Numericos",
        size=34,
        weight=ft.FontWeight.BOLD,
        color="#38bdf8"
    )

    subtitulo = ft.Text(
        "Biseccion y Secante con FastAPI + Flet",
        size=16,
        color="#cbd5e1"
    )

    # =====================================================
    # CONFIGURACION BACKEND
    # =====================================================

    ip_backend = ft.TextField(
        label="IP Backend",
        value="https://basically-reprocess-sensitize.ngrok-free.dev",
        width=350,
        **ESTILO_INPUT
    )

    # =====================================================
    # METODOS
    # =====================================================

    metodo = ft.Dropdown(
        label="Metodo",
        width=350,
        value="biseccion",
        bgcolor="#1e293b",
        border_color="#38bdf8",
        color="white",
        border_radius=15,
        options=[
            ft.dropdown.Option("biseccion"),
            ft.dropdown.Option("secante"),
        ],
    )

    # =====================================================
    # ENTRADAS
    # =====================================================

    funcion = ft.TextField(
        label="Funcion",
        value="x**2 - 5",
        width=350,
        **ESTILO_INPUT
    )

    valor1 = ft.TextField(
        label="a / x0",
        value="2",
        width=350,
        **ESTILO_INPUT
    )

    valor2 = ft.TextField(
        label="b / x1",
        value="3",
        width=350,
        **ESTILO_INPUT
    )

    tolerancia = ft.TextField(
        label="Tolerancia",
        value="0.001",
        width=350,
        **ESTILO_INPUT
    )

    max_iter = ft.TextField(
        label="Max Iteraciones",
        value="50",
        width=350,
        **ESTILO_INPUT
    )

    # =====================================================
    # RESULTADOS
    # =====================================================

    resultado_texto = ft.Text(
        size=16,
        color="#22c55e"
    )

    # =====================================================
    # TABLA
    # =====================================================

    tabla = ft.DataTable(

        heading_row_color="#1e293b",

        columns=[
            ft.DataColumn(
                ft.Text(
                    "Iteracion",
                    color="white"
                )
            ),

            ft.DataColumn(
                ft.Text(
                    "x",
                    color="white"
                )
            ),

            ft.DataColumn(
                ft.Text(
                    "f(x)",
                    color="white"
                )
            ),

            ft.DataColumn(
                ft.Text(
                    "Error",
                    color="white"
                )
            ),
        ],

        rows=[]
    )

    # =====================================================
    # FUNCION RESOLVER
    # =====================================================

    def resolver(e):

        tabla.rows.clear()

        try:

            url = f"{ip_backend.value}/{metodo.value}"

            if metodo.value == "biseccion":

                datos = {
                    "funcion": funcion.value,
                    "a": float(valor1.value),
                    "b": float(valor2.value),
                    "tolerancia": float(tolerancia.value),
                    "max_iteraciones": int(max_iter.value)
                }

            else:

                datos = {
                    "funcion": funcion.value,
                    "x0": float(valor1.value),
                    "x1": float(valor2.value),
                    "tolerancia": float(tolerancia.value),
                    "max_iteraciones": int(max_iter.value)
                }

            headers = {
                "ngrok-skip-browser-warning": "true"
            }

            respuesta = requests.post(
                url,
                json=datos,
                headers=headers,
                timeout=20
            )

            if respuesta.status_code == 200:

                data = respuesta.json()

                resultado_texto.value = (
                    f"Raiz aproximada: {data['raiz_aproximada']}\n"
                    f"Iteraciones: {data['iteraciones_totales']}\n"
                    f"Error final: {data['error_final']}\n"
                    f"Convergencia: {data['convergencia']}"
                )

                resultado_texto.color = "#22c55e"

                for item in data["iteraciones"]:

                    if metodo.value == "biseccion":
                        x = item.get("c", "")
                        fx = item.get("f_c", "")
                    else:
                        x = item.get("x_nuevo", "")
                        fx = item.get("f_x_n", "")

                    tabla.rows.append(
                        ft.DataRow(
                            cells=[

                                ft.DataCell(
                                    ft.Text(
                                        str(item.get("iteracion", "")),
                                        color="white"
                                    )
                                ),

                                ft.DataCell(
                                    ft.Text(
                                        str(x),
                                        color="#38bdf8"
                                    )
                                ),

                                ft.DataCell(
                                    ft.Text(
                                        str(fx),
                                        color="#facc15"
                                    )
                                ),

                                ft.DataCell(
                                    ft.Text(
                                        str(item.get("error", "")),
                                        color="#22c55e"
                                    )
                                ),
                            ]
                        )
                    )

            else:

                resultado_texto.value = (
                    f"Error del servidor:\n{respuesta.text}"
                )

                resultado_texto.color = "red"

        except Exception as ex:

            resultado_texto.value = (
                f"Error de conexion:\n{str(ex)}"
            )

            resultado_texto.color = "red"

        page.update()

    # =====================================================
    # BOTON
    # =====================================================

    boton = ft.ElevatedButton(
        "Resolver",
        icon=ft.Icons.CALCULATE,
        on_click=resolver,

        style=ft.ButtonStyle(
            bgcolor="#0ea5e9",
            color="white",
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),

        width=350,
        height=55
    )

    # =====================================================
    # PANEL IZQUIERDO
    # =====================================================

    izquierda = ft.Container(

        content=ft.Column(
            [
                titulo,
                subtitulo,

                ft.Divider(color="#334155"),

                ip_backend,
                metodo,
                funcion,
                valor1,
                valor2,
                tolerancia,
                max_iter,
                boton,
            ],

            spacing=18
        ),

        padding=25,
        width=420,
        bgcolor="#111827",
        border_radius=25,
    )

    # =====================================================
    # PANEL DERECHO
    # =====================================================

    derecha = ft.Container(

        content=ft.Column(
            [

                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ANALYTICS,
                            color="#38bdf8"
                        ),

                        ft.Text(
                            "Resultados",
                            size=28,
                            weight="bold",
                            color="white"
                        ),
                    ]
                ),

                ft.Divider(color="#334155"),

                resultado_texto,

                ft.Text(
                    "Tabla de Iteraciones",
                    size=22,
                    weight="bold",
                    color="#38bdf8"
                ),

                ft.Container(
                    content=ft.Column(
                        [tabla],
                        scroll="auto"
                    ),
                    height=500
                )
            ]
        ),

        padding=25,
        expand=True,
        bgcolor="#111827",
        border_radius=25,
    )

    # =====================================================
    # CREDITOS
    # =====================================================

    creditos = ft.Text(
        "Hecho por Jose Urrunaga, Felix Samudio, Jeremy Gonzales",
        size=12,
        color="#94a3b8",
        italic=True
    )

    # =====================================================
    # LAYOUT
    # =====================================================

    page.add(

        ft.Container(

            content=ft.Column(
                [

                    ft.Row(
                        [
                            izquierda,
                            derecha
                        ],

                        expand=True,
                        spacing=25,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START
                    ),

                    ft.Row(
                        [
                            creditos
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ]
            ),

            padding=10
        )
    )


ft.app(target=main)
