import flet as ft


def crear_header(page: ft.Page, ir_a, titulo="UniRuta"):
    # 1. Obtener objeto usuario y su foto actual
    usuario = getattr(page, "usuario_actual", None)
    foto_usuario = getattr(usuario, "foto", None) if usuario else None

    # 2. Crear avatar dinámico (Si hay foto se muestra la imagen, si no, el icono)
    avatar_contenido = ft.CircleAvatar(
        radius=18,
        bgcolor="#0E4A5B",
        foreground_image_src=foto_usuario if foto_usuario else None,
        content=(
            ft.Icon(ft.Icons.PERSON, size=20, color="white")
            if not foto_usuario
            else None
        ),
    )

    # 3. Botón de perfil interactivo
    btn_perfil = ft.Container(
        content=avatar_contenido,
        ink=True,
        on_click=lambda e: ir_a("perfil"),
        tooltip="Mi Perfil",
        border_radius=20,
    )

    # 4. Estructura del Header
    return ft.Container(
        height=60,
        bgcolor="white",
        padding=ft.Padding(20, 0, 20, 0),
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.DIRECTIONS_BUS, color="#0E4A5B", size=26),
                        ft.Text(
                            titulo,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#0E4A5B",
                        ),
                    ],
                ),
                btn_perfil,
            ],
        ),
    )