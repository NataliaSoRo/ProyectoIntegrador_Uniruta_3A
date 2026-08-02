import flet as ft
from components.sidebar import sidebar
from components.topbar import topbar
from components.toolbar import toolbar
from components.tabla_viajes import tabla_viajes

def vista_viajes(page: ft.Page):

    return ft.Row(

        expand=True,

        controls=[

            sidebar(),

            ft.Container(

                expand=True,

                bgcolor="#F5F5F5",

                content=ft.Column(

                    spacing=0,

                    controls=[

                        topbar(),

                        ft.Container(

                            padding=30,

                            content=ft.Text(

                                "Viajes",

                                size=34,

                                weight=ft.FontWeight.BOLD,

                            ),
                        ),

                        ft.Container(
                            padding=30,
                            content=toolbar(page),
                        ),

                        ft.Container(
                            padding=30,
                            content=tabla_viajes(),
                        ),

                    ],
                ),
            ),
        ],
    )