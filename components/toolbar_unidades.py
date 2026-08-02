import flet as ft


def toolbar_unidades():

    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

        controls=[

            ft.Container(
                width=350,

                content=ft.TextField(
                    hint_text="Buscar unidad...",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=12,
                    filled=True,
                    bgcolor="white",
                ),
            ),

            ft.ElevatedButton(
                "Agregar unidad",
                icon=ft.Icons.ADD,

                bgcolor="#F4B400",
                color="white",

                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=20,
                ),
            ),
        ],
    )