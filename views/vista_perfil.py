import flet as ft


def vista_perfil(page: ft.Page, ir_a, ruta_previa="menu_principal"):
    page.title = "UniRuta - Mi Perfil"

    usuario = getattr(page, "usuario_actual", None)
    nombre_inicial = getattr(usuario, "nombre", "Natalia Sosa Rodriguez") if usuario else "Natalia Sosa Rodriguez"
    rol_inicial = getattr(usuario, "rol", "admin") if usuario else "admin"
    correo_inicial = getattr(usuario, "correo", getattr(usuario, "email", "seojinlee278@gmail.com")) if usuario else "seojinlee278@gmail.com"
    foto_inicial = getattr(usuario, "foto", None) if usuario else None

    es_editable = False

    txt_nombre = ft.TextField(value=nombre_inicial, read_only=True, label="Nombre completo", height=45)
    txt_correo = ft.TextField(value=correo_inicial, read_only=True, label="Correo electrónico", height=45)
    txt_rol = ft.TextField(value=rol_inicial, read_only=True, label="Rol / Cargo", height=45)

    txt_foto_url = ft.TextField(
        label="Ruta o URL de la foto de perfil",
        height=45,
        visible=False,
        value=foto_inicial or "",
        hint_text="Ej: assets/foto.png o https://...",
    )

    avatar_perfil = ft.CircleAvatar(
        radius=50,
        bgcolor="#0E4A5B",
        foreground_image_src=foto_inicial if foto_inicial else None,
        content=ft.Icon(ft.Icons.PERSON, size=50, color="white") if not foto_inicial else None,
    )

    def cambiar_foto_input(e):
        txt_foto_url.visible = not txt_foto_url.visible
        page.update()

    btn_cambiar_foto = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT,
        icon_color="white",
        bgcolor="#EC932F",
        icon_size=18,
        tooltip="Cambiar foto de perfil",
        visible=False,
        on_click=cambiar_foto_input,
    )

    def alternar_edicion(e):
        nonlocal es_editable
        es_editable = not es_editable

        txt_nombre.read_only = not es_editable
        txt_correo.read_only = not es_editable
        txt_rol.read_only = not es_editable

        btn_cambiar_foto.visible = es_editable
        btn_editar.visible = not es_editable
        acciones_edicion.visible = es_editable
        if not es_editable:
            txt_foto_url.visible = False

        page.update()

    def guardar_cambios(e):
        nueva_foto = txt_foto_url.value.strip() if txt_foto_url.value else None

        if nueva_foto:
            avatar_perfil.foreground_image_src = nueva_foto
            avatar_perfil.content = None

        # Guardar cambios en el estado global de la página
        if not hasattr(page, "usuario_actual") or page.usuario_actual is None:
            class Usuario: pass
            page.usuario_actual = Usuario()

        page.usuario_actual.nombre = txt_nombre.value
        page.usuario_actual.correo = txt_correo.value
        page.usuario_actual.rol = txt_rol.value
        page.usuario_actual.foto = nueva_foto

        alternar_edicion(e)

        snack = ft.SnackBar(
            content=ft.Text("Perfil actualizado correctamente"),
            bgcolor="#10B981",
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    btn_editar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.EDIT, size=16, color="white"),
                ft.Text("Editar Perfil", color="white"),
            ],
            tight=True,
        ),
        bgcolor="#0E4A5B",
        on_click=alternar_edicion,
    )

    acciones_edicion = ft.Row(
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.OutlinedButton("Cancelar", on_click=alternar_edicion),
            ft.ElevatedButton(
                "Guardar",
                bgcolor="#EC932F",
                color="white",
                on_click=guardar_cambios,
            ),
        ],
    )

    imagen_perfil_container = ft.Stack(
        controls=[
            avatar_perfil,
            ft.Container(
                content=btn_cambiar_foto,
                right=0,
                bottom=0,
            ),
        ],
        width=100,
        height=100,
    )

    # El botón de volver regresa dinámicamente a la 'ruta_previa'
    header = ft.Container(
        height=58,
        bgcolor="white",
        padding=ft.Padding(15, 0, 20, 0),
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("UniRuta", size=18, weight=ft.FontWeight.BOLD, color="#0E4A5B"),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="Volver",
                    on_click=lambda e: ir_a(ruta_previa),
                ),
            ],
        ),
    )

    tarjeta_perfil = ft.Container(
        width=450,
        bgcolor="white",
        border_radius=12,
        padding=25,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                imagen_perfil_container,
                ft.Text(
                    "Información del Usuario",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#1E293B",
                ),
                txt_nombre,
                txt_correo,
                txt_rol,
                txt_foto_url,
                ft.Divider(height=10, color="transparent"),
                btn_editar,
                acciones_edicion,
            ],
        ),
    )

    area_trabajo = ft.Container(
        expand=True,
        bgcolor="#FAFAFA",
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=tarjeta_perfil,
    )

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[header, area_trabajo],
    )