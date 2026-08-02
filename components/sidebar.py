import flet as ft

def boton_menu(icono, texto, on_click=None, seleccionado=False):

    return ft.Container(
        on_click=on_click,
        bgcolor="#4D91A8" if seleccionado else None,
        border_radius=10,
        padding=10,

        content=ft.Row(
            controls=[
                ft.Icon(
                    icono,
                    color="white",
                    size=22
                ),

                ft.Text(
                    texto,
                    color="white",
                    size=16
                )
            ]
        )
    )

def sidebar(page, vista_actual):

    return ft.Container(
        width=250,
        bgcolor="#79B6C9",
        padding=20,

        content=ft.Column(

            spacing=15,

            controls=[

                ft.Text(
                    "UniRuta",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                ft.Divider(color="white"),

                boton_menu(
                    ft.Icons.HOME,
                    "Menú principal",
                    seleccionado=vista_actual == "menu"
                ),

                boton_menu(
                    ft.Icons.BADGE,
                    "Choferes",
                    seleccionado=vista_actual == "choferes"
                ),

                boton_menu(
                    ft.Icons.DIRECTIONS_BUS,
                    "Unidades",
                    seleccionado=vista_actual == "unidades"
                ),

                boton_menu(
                    ft.Icons.MAP,
                    "Rutas",
                    seleccionado=vista_actual == "rutas"
                ),

                boton_menu(
                    ft.Icons.LUGGAGE,
                    "Viajes",
                    seleccionado=vista_actual == "viajes"
                ),

                boton_menu(
                    ft.Icons.PAYMENTS,
                    "Pagos",
                    seleccionado=vista_actual == "pagos"
                ),
               
            ]
        )
    )