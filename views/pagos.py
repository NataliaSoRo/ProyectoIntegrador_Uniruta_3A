import flet as ft

try:
    from dao.pagos_dao import PagoDAO
except ImportError:
    PagoDAO = None


def vista_pagos(page: ft.Page, ir_a):
    page.title = "UniRuta - Pagos"

    dao = PagoDAO() if PagoDAO else None

    # Usuario actual de la sesión
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = (
        getattr(usuario, "nombre", "Natalia Sosa Rodriguez")
        if usuario
        else "Natalia Sosa Rodriguez"
    )
    rol_usuario = getattr(usuario, "rol", "admin") if usuario else "admin"

    estado_sesion = {"acceso_concedido": False}

    # --- LÓGICA DE NAVEGACIÓN Y PERFIL ---
    def cerrar_sesion(e):
        if hasattr(page, "usuario_actual"):
            page.usuario_actual = None
        ir_a("login")

    def ir_al_perfil(e):
        ir_a("perfil")

    def abrir_notificaciones(e):
        dialogo = ft.AlertDialog(
            title=ft.Text("Notificaciones", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ATTACH_MONEY, color="#3B82F6"),
                        title=ft.Text("Pagos pendientes", size=13),
                        subtitle=ft.Text(
                            "Revisa los pagos pendientes del periodo.", size=11
                        ),
                    ),
                ],
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=lambda e: setattr(dialogo, "open", False)
                    or page.update(),
                )
            ],
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    # --- 1. HEADER REUTILIZABLE ---
    logo_header = ft.Container(
        padding=ft.Padding(10, 0, 0, 0),
        on_click=lambda e: ir_a("menu_principal"),
        content=ft.Image(src="logo_uniruta.png", height=38, fit="contain"),
    )

    info_usuario = ft.Row(
        spacing=12,
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.Stack(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                        icon_color="#64748B",
                        icon_size=22,
                        tooltip="Notificaciones",
                        on_click=abrir_notificaciones,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "1",
                            size=9,
                            color="white",
                            weight=ft.FontWeight.BOLD,
                        ),
                        bgcolor="#EF4444",
                        border_radius=8,
                        padding=ft.Padding(4, 2, 4, 2),
                        right=4,
                        top=4,
                    ),
                ]
            ),
            ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=[
                    ft.Text(
                        nombre_usuario,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color="#1E293B",
                    ),
                    ft.Text(rol_usuario, size=11, color="#64748B"),
                ],
            ),
            ft.PopupMenuButton(
                content=ft.Container(
                    width=34,
                    height=34,
                    border=ft.Border.all(1, "#CBD5E1"),
                    border_radius=17,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#F1F5F9",
                    on_click=ir_al_perfil,
                    content=ft.Icon(
                        ft.Icons.PERSON_OUTLINE, size=18, color="#475569"
                    ),
                ),
                items=[
                    ft.PopupMenuItem(
                        icon=ft.Icons.PERSON_OUTLINE,
                        content=ft.Text("Mi Perfil", size=13),
                        on_click=ir_al_perfil,
                    ),
                    ft.PopupMenuItem(
                        icon=ft.Icons.SETTINGS_OUTLINED,
                        content=ft.Text("Configuración", size=13),
                        on_click=lambda e: ir_a("configuracion"),
                    ),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(
                        icon=ft.Icons.LOGOUT,
                        content=ft.Text("Cerrar sesión", size=13),
                        on_click=cerrar_sesion,
                    ),
                ],
            ),
        ],
    )

    header = ft.Container(
        height=60,
        bgcolor="white",
        padding=ft.Padding(15, 0, 20, 0),
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        shadow=ft.BoxShadow(
            blur_radius=4,
            color=ft.Colors.with_opacity(0.05, "black"),
            offset=ft.Offset(0, 2),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[logo_header, info_usuario],
        ),
    )

    # --- 2. SIDEBAR LATERAL ---
    def item_sidebar(texto, icono, ruta, activo=False):
        bg = "#0E4A5B" if activo else ft.Colors.TRANSPARENT
        color_txt = "white" if activo else "#1E293B"
        color_ico = "white" if activo else "#334155"

        return ft.Container(
            padding=ft.Padding(18, 12, 18, 12),
            bgcolor=bg,
            on_click=lambda e: ir_a(ruta) if ruta else None,
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(icono, color=color_ico, size=20),
                    ft.Text(
                        texto,
                        color=color_txt,
                        size=13,
                        weight=(
                            ft.FontWeight.BOLD
                            if activo
                            else ft.FontWeight.W_500
                        ),
                    ),
                ],
            ),
        )

    sidebar = ft.Container(
        width=190,
        bgcolor="#7CAFC4",
        content=ft.Column(
            spacing=2,
            controls=[
                ft.Container(
                    padding=ft.Padding(12, 8, 12, 4),
                    content=ft.IconButton(
                        icon=ft.Icons.MENU, icon_color="#1E293B"
                    ),
                ),
                item_sidebar(
                    "Menú principal", ft.Icons.HOME_OUTLINED, "menu_principal"
                ),
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes"),
                item_sidebar(
                    "Unidades", ft.Icons.DIRECTIONS_BUS_OUTLINED, "unidades"
                ),
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar(
                    "Pagos", ft.Icons.ATTACH_MONEY, "pagos", activo=True
                ),
            ],
        ),
    )

    # --- 3. VISTA MODAL / FORMULARIO INICIAL DE INGRESO (TARJETA PROTOTIPO) ---
    txt_correo_auth = ft.TextField(
        hint_text="juanperez@gmail.com",
        width=290,
        height=40,
        text_size=12,
        border_color="#D1D5DB",
        focused_border_color="#6B66F6",
        content_padding=ft.Padding(12, 8, 12, 8),
    )
    txt_pass_auth = ft.TextField(
        hint_text="********",
        password=True,
        can_reveal_password=True,
        width=290,
        height=40,
        text_size=12,
        border_color="#D1D5DB",
        focused_border_color="#6B66F6",
        content_padding=ft.Padding(12, 8, 12, 8),
    )
    lbl_error_auth = ft.Text("", size=11, color="#EF4444")

    def validar_acceso_pagos(e):
        if txt_correo_auth.value and txt_pass_auth.value:
            estado_sesion["acceso_concedido"] = True
            area_trabajo.content = contenido_tabla_pagos
            page.update()
        else:
            lbl_error_auth.value = "Por favor ingrese correo y contraseña."
            page.update()

    card_autenticacion = ft.Container(
        width=420,
        padding=ft.Padding(40, 45, 40, 45),
        bgcolor="white",
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=25,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.15, "black"),
            offset=ft.Offset(0, 8),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.Text(
                    "Ingrese sus datos",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                ft.Text(
                    "Solo administradores pueden tener\nacceso al apartado de pagos",
                    size=12,
                    color="#64748B",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("Correo electronico", size=11, color="#4B5563"),
                        txt_correo_auth,
                    ],
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Text("Contraseña", size=11, color="#4B5563"),
                        txt_pass_auth,
                    ],
                ),
                lbl_error_auth,
                ft.Container(height=12),
                ft.ElevatedButton(
                    content=ft.Text(
                        "Aceptar",
                        color="white",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                    ),
                    bgcolor="#6B66F6",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        padding=ft.Padding(50, 12, 50, 12),
                        elevation=2,
                    ),
                    on_click=validar_acceso_pagos,
                ),
            ],
        ),
    )

    contenido_login_pagos = ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                width=680,
                height=680,
                bgcolor="#82B3C9",
                border_radius=340,
                right=-120,
                bottom=-180,
            ),
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(height=20),
                    ft.Text(
                        "Pagos",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1E293B",
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, -0.15),
                        content=card_autenticacion,
                    ),
                ],
            ),
        ],
    )

    # --- 4. VISTA DE TABLA COMPLETA ---
    tabla_pagos = ft.DataTable(
        bgcolor="white",
        heading_row_color="#FC9210",
        heading_row_height=40,
        data_row_min_height=52,
        column_spacing=18,
        columns=[
            ft.DataColumn(
                ft.Text("ID", color="white", size=11, weight=ft.FontWeight.BOLD)
            ),
            ft.DataColumn(
                ft.Text(
                    "ID Viaje",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Chofer asignado",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Pago base",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "pago inicial",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Pago final",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Total acumulado",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Metodo pago",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Periodo de pago",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Acciones",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
        ],
        rows=[],
    )

    def eliminar_pago(id_pago):
        if dao and hasattr(dao, "eliminar") and dao.eliminar(id_pago):
            cargar_datos_tabla()
            page.update()

    def cargar_datos_tabla(filtro=""):
        lista = []
        if dao:
            if filtro.strip() and hasattr(dao, "buscar"):
                lista = dao.buscar(filtro)
            elif hasattr(dao, "obtener_todos"):
                lista = dao.obtener_todos()

        filas = []
        for idx, p in enumerate(lista, start=1):
            metodo = str(getattr(p, "metodo_pago", "") or "Pago en Tarjeta")
            es_efectivo = "efectivo" in metodo.lower()

            icono_metodo = (
                ft.Icons.MONEY if es_efectivo else ft.Icons.CREDIT_CARD
            )
            color_metodo = "#10B981" if es_efectivo else "#2563EB"

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(getattr(p, "id", idx)),
                                size=11,
                                color="#1E293B",
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(getattr(p, "id_viaje", None) or "V-024"),
                                size=11,
                                color="#475569",
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Icon(
                                            ft.Icons.PERSON,
                                            size=14,
                                            color="white",
                                        ),
                                        bgcolor="#93C5FD",
                                        radius=12,
                                    ),
                                    ft.Text(
                                        str(
                                            getattr(p, "chofer", None)
                                            or getattr(
                                                p,
                                                "chofer_asignado",
                                                "Juan Pérez",
                                            )
                                        ),
                                        size=11,
                                        color="#1E293B",
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ],
                                spacing=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                f"${getattr(p, 'pago_base', 4000):.2f}",
                                size=11,
                                color="#1E293B",
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                bgcolor="#F1F5F9",
                                border_radius=6,
                                padding=ft.Padding(6, 2, 6, 2),
                                content=ft.Text(
                                    f"${getattr(p, 'pago_inicial', 4000):.2f}",
                                    size=11,
                                    color="#1E293B",
                                    weight=ft.FontWeight.BOLD,
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                f"${getattr(p, 'pago_final', 4000):.2f}",
                                size=11,
                                color="#1E293B",
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                f"${getattr(p, 'total_acumulado', 4000):.2f}",
                                size=11,
                                color="#1E293B",
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(
                                        icono_metodo,
                                        size=16,
                                        color=color_metodo,
                                    ),
                                    ft.Text(
                                        metodo,
                                        size=11,
                                        color=color_metodo,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ],
                                spacing=4,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(
                                    getattr(
                                        p, "periodo_pago", "Quincenal"
                                    )
                                ),
                                size=11,
                                color="#475569",
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#F97316"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=lambda e, id_p=getattr(
                                            p, "id", None
                                        ): print(f"Editar {id_p}"),
                                        content=ft.Icon(
                                            ft.Icons.EDIT_OUTLINED,
                                            size=13,
                                            color="#F97316",
                                        ),
                                    ),
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#EF4444"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=lambda e, id_p=getattr(
                                            p, "id", None
                                        ): eliminar_pago(id_p),
                                        content=ft.Icon(
                                            ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            size=13,
                                            color="#EF4444",
                                        ),
                                    ),
                                ],
                                spacing=6,
                            )
                        ),
                    ]
                )
            )
        tabla_pagos.rows = filas

    def al_cambiar_buscador(e):
        cargar_datos_tabla(e.control.value)
        page.update()

    buscador = ft.TextField(
        hint_text="Busca chofer",
        prefix_icon=ft.Icons.SEARCH,
        height=38,
        content_padding=ft.Padding(12, 0, 12, 0),
        border_radius=19,
        bgcolor="white",
        border_color="#CBD5E1",
        focused_border_color="#FC9210",
        text_size=12,
        on_change=al_cambiar_buscador,
    )

    btn_agregar_pago = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ADD, color="white", size=16),
                ft.Text(
                    "Agregar pago",
                    color="white",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=4,
        ),
        bgcolor="#FC9210",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=18),
            padding=ft.Padding(16, 8, 16, 8),
        ),
        on_click=lambda e: print("Abrir formulario agregar pago"),
    )

    barra_controles = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[ft.Container(width=420, content=buscador), btn_agregar_pago],
    )

    cargar_datos_tabla()

    contenedor_tabla = ft.Container(
        bgcolor="white",
        border_radius=8,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 3),
        ),
        content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[tabla_pagos]),
    )

    contenido_tabla_pagos = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Pagos",
                size=22,
                weight=ft.FontWeight.BOLD,
                color="#000000",
            ),
            barra_controles,
            contenedor_tabla,
        ],
    )

    area_trabajo = ft.Container(
        expand=True,
        bgcolor="#FAFAFA",
        padding=ft.Padding(25, 15, 25, 20),
        content=contenido_login_pagos,
    )

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            header,
            ft.Row(
                expand=True,
                spacing=0,
                controls=[sidebar, area_trabajo],
            ),
        ],
    )