import flet as ft

from components.sidebar import sidebar
from components.topbar import topbar
from components.toolbar_unidades import toolbar_unidades


def vista_unidades(page):

    return ft.Row(

        controls=[

            sidebar(page, "unidades"),

            ft.Container(

                expand=True,

                padding=20,

                bgcolor="#F5F5F5",

                content=ft.Column(

                    controls=[

                        topbar(),

                        ft.Text(
                            "Unidades",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                        ),

                        toolbar_unidades(),

                    ],

                    spacing=20,
                ),
            ),
        ],

        expand=True,
    )