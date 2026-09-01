import flet as ft


# ============================================================
# CONFIGURACIÓN DEL EDITOR
# ============================================================

GRID_SIZE = 8
TOTAL_BITS = 64

COLOR_APAGADO = "#151A21"
COLOR_ENCENDIDO = "#00E676"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main(page: ft.Page):

    # --------------------------------------------------------
    # CONFIGURACIÓN DE LA VENTANA
    # --------------------------------------------------------

    page.title = "Editor de Sprites 8x8 - CUL"

    page.theme_mode = ft.ThemeMode.DARK

    page.padding = 25

    # --------------------------------------------------------
    # MATRIZ DE PÍXELES
    # --------------------------------------------------------

    pixels = []

    for fila in range(GRID_SIZE):

        fila_pixels = []

        for columna in range(GRID_SIZE):

            pixel = ft.Container(
                width=55,
                height=55,
                bgcolor=COLOR_APAGADO,
                border_radius=5,
                ink=True,
            )

            fila_pixels.append(pixel)

        pixels.append(fila_pixels)

    # ========================================================
    # ELEMENTOS DE INFORMACIÓN
    # ========================================================

    hex_output = ft.Text(
        "0000000000000000",
        size=28,
        weight=ft.FontWeight.BOLD,
    )

    binary_output = ft.Text(
        "0" * TOTAL_BITS,
        size=14,
        selectable=True,
    )

    mensaje = ft.Text(
        "Listo para editar el sprite.",
        size=14,
    )

    # ========================================================
    # CAMPO DE ENTRADA HEXADECIMAL
    # ========================================================

    hex_input = ft.TextField(
        label="Código hexadecimal",
        hint_text="Ej: FF818181818181FF",
        max_length=16,
        width=400,
    )

    # ========================================================
    # FUNCIÓN: LEER LA MATRIZ
    # ========================================================

    def obtener_binario():

        bits = ""

        for fila in range(GRID_SIZE):

            for columna in range(GRID_SIZE):

                pixel = pixels[fila][columna]

                if pixel.bgcolor == COLOR_ENCENDIDO:

                    bits += "1"

                else:

                    bits += "0"

        return bits

    # ========================================================
    # FUNCIÓN: BINARIO A HEXADECIMAL
    # ========================================================

    def binario_a_hexadecimal(binary):

        numero = int(binary, 2)

        hexadecimal = format(numero, "016X")

        return hexadecimal

    # ========================================================
    # FUNCIÓN: ACTUALIZAR HEX Y BINARIO
    # ========================================================

    def actualizar_codigo():

        binary = obtener_binario()

        hexadecimal = binario_a_hexadecimal(binary)

        binary_output.value = binary

        hex_output.value = hexadecimal

        page.update()

    # ========================================================
    # FUNCIÓN: ENCENDER / APAGAR PÍXEL
    # ========================================================

    def cambiar_pixel(e):

        pixel = e.control

        if pixel.bgcolor == COLOR_APAGADO:

            pixel.bgcolor = COLOR_ENCENDIDO

        else:

            pixel.bgcolor = COLOR_APAGADO

        actualizar_codigo()

    # ========================================================
    # ASIGNAR EVENTO A LOS 64 PÍXELES
    # ========================================================

    for fila in range(GRID_SIZE):

        for columna in range(GRID_SIZE):

            pixels[fila][columna].on_click = cambiar_pixel

    # ========================================================
    # CREAR GRIDVIEW
    # ========================================================

    grid = ft.GridView(
        runs_count=8,
        spacing=6,
        run_spacing=6,
        width=500,
        height=500,
    )

    # Agregar los 64 píxeles al GridView

    for fila in range(GRID_SIZE):

        for columna in range(GRID_SIZE):

            grid.controls.append(
                pixels[fila][columna]
            )

    # ========================================================
    # FUNCIÓN: CARGAR HEXADECIMAL
    # ========================================================

    def cargar_hex(e):

        valor = hex_input.value.strip().upper()

        # ----------------------------------------------------
        # COMPROBAR QUE NO ESTÉ VACÍO
        # ----------------------------------------------------

        if valor == "":

            mensaje.value = "Escribe un código hexadecimal."

            page.update()

            return

        # ----------------------------------------------------
        # COMPROBAR LONGITUD
        # ----------------------------------------------------

        if len(valor) > 16:

            mensaje.value = (
                "Error: el código hexadecimal debe tener "
                "máximo 16 caracteres."
            )

            page.update()

            return

        # ----------------------------------------------------
        # INTENTAR CONVERTIR HEXADECIMAL
        # ----------------------------------------------------

        try:

            numero = int(valor, 16)

        except ValueError:

            mensaje.value = (
                "Error: solo se permiten caracteres "
                "0-9 y A-F."
            )

            page.update()

            return

        # ----------------------------------------------------
        # CONVERTIR A 64 BITS
        # ----------------------------------------------------

        binary = format(numero, "064b")

        # ----------------------------------------------------
        # COLOCAR LOS BITS EN LA MATRIZ
        # ----------------------------------------------------

        indice = 0

        for fila in range(GRID_SIZE):

            for columna in range(GRID_SIZE):

                bit = binary[indice]

                if bit == "1":

                    pixels[fila][columna].bgcolor = (
                        COLOR_ENCENDIDO
                    )

                else:

                    pixels[fila][columna].bgcolor = (
                        COLOR_APAGADO
                    )

                indice += 1

        # ----------------------------------------------------
        # ACTUALIZAR INFORMACIÓN
        # ----------------------------------------------------

        binary_output.value = binary

        hex_output.value = format(numero, "016X")

        mensaje.value = "Hexadecimal cargado correctamente."

        page.update()

    # ========================================================
    # FUNCIÓN: LIMPIAR MATRIZ
    # ========================================================

    def limpiar(e):

        for fila in range(GRID_SIZE):

            for columna in range(GRID_SIZE):

                pixels[fila][columna].bgcolor = (
                    COLOR_APAGADO
                )

        hex_input.value = ""

        binary_output.value = "0" * TOTAL_BITS

        hex_output.value = "0000000000000000"

        mensaje.value = "Matriz limpiada."

        page.update()

    # ========================================================
    # BOTÓN CARGAR HEX
    # ========================================================

    cargar_button = ft.FilledButton(
        content="Cargar Hex",
        on_click=cargar_hex,
    )

    # ========================================================
    # BOTÓN LIMPIAR
    # ========================================================

    limpiar_button = ft.FilledButton(
        content="Limpiar",
        on_click=limpiar,
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    titulo = ft.Text(
        "EDITOR DE SPRITES 8 × 8",
        size=32,
        weight=ft.FontWeight.BOLD,
    )

    subtitulo = ft.Text(
        "Editor de mapas de bits de 64 bits",
        size=16,
    )

    # ========================================================
    # PANEL HEXADECIMAL
    # ========================================================

    panel_hex = ft.Container(

        padding=20,

        border_radius=12,

        bgcolor="#20252D",

        content=ft.Column(

            controls=[

                ft.Text(
                    "CÓDIGO HEXADECIMAL",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),

                hex_output,

                ft.Divider(),

                hex_input,

                ft.Row(
                    controls=[
                        cargar_button,
                        limpiar_button,
                    ],
                    spacing=10,
                ),

                mensaje,

            ],

            spacing=15,

        ),

    )

    # ========================================================
    # PANEL BINARIO
    # ========================================================

    panel_binario = ft.Container(

        padding=15,

        border_radius=10,

        bgcolor="#20252D",

        content=ft.Column(

            controls=[

                ft.Text(
                    "BINARIO (64 BITS)",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),

                binary_output,

            ]

        ),

    )

    # ========================================================
    # PANEL DE LA MATRIZ
    # ========================================================

    panel_matriz = ft.Column(

        controls=[

            ft.Text(
                "MATRIZ DE PÍXELES",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),

            grid,

            ft.Text(
                "Haz clic sobre los píxeles para "
                "encenderlos o apagarlos.",
                size=14,
            ),

        ],

        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

    )

    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    page.add(

        ft.Column(

            controls=[

                titulo,

                subtitulo,

                ft.Divider(),

                ft.Row(

                    controls=[

                        panel_matriz,

                        ft.Column(

                            controls=[

                                panel_hex,

                                panel_binario,

                            ],

                            width=420,

                            spacing=20,

                        ),

                    ],

                    alignment=ft.MainAxisAlignment.CENTER,

                    vertical_alignment=(
                        ft.CrossAxisAlignment.START
                    ),

                ),

            ],

            spacing=15,

        )

    )


# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    ft.run(main)