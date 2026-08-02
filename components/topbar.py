import flet as ft

def topbar():

    return ft.Container(
        height=70,
        bgcolor="white",
        padding=20,

        content=ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.Text(
                    "Panel de Administración",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(

                    spacing=20,

                    controls=[

                        ft.Icon(
                            ft.Icons.NOTIFICATIONS_NONE,
                            size=28,
                        ),

                        ft.CircleAvatar(
                            content=ft.Text("A"),
                            bgcolor="#79B6C9",
                            color="white",
                        ),
                    ],
                ),
            ],
        ),
    )