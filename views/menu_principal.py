import flet as ft

from dao.kpi_dao import KpiDAO


def vista_menu_principal(page: ft.Page, ir_a):
    page.title = "UniRuta - Menú Principal"

    # --- OBTENER DATOS DE LA BD ---
    dao = KpiDAO()
    resumen = dao.obtener_resumen_kpis()
    prioridades = dao.obtener_prioridades()

    # Usuario actual de la sesión (fallback a "Juana Suarez" si no hay datos)
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = (
        getattr(usuario, "nombre", "Juana Suarez") if usuario else "Juana Suarez"
    )
    rol_usuario = (
        getattr(usuario, "rol", "Administrador") if usuario else "Administrador"
    )

    # --- LÓGICA DE DIÁLOGOS Y SESIÓN ---
    def cerrar_sesion(e):
        if hasattr(page, "usuario_actual"):
            page.usuario_actual = None
        ir_a("login")

    def cerrar_dialogo(dialogo):
        dialogo.open = False
        page.update()

    def abrir_notificaciones(e):
        dialogo = ft.AlertDialog(
            title=ft.Text("Notificaciones", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BADGE_OUTLINED, color="#3B82F6"),
                        title=ft.Text("Licencia por vencer", size=13),
                        subtitle=ft.Text(
                            "Revisa la vigencia de los choferes.", size=11
                        ),
                    ),
                ],
            ),
            actions=[
                ft.TextButton(
                    "Cerrar", on_click=lambda e: cerrar_dialogo(dialogo)
                )
            ],
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    # --- 1. BARRA SUPERIOR (HEADER UNIFICADO) ---
    logo_header = ft.Container(
        padding=ft.Padding(15, 8, 15, 8),
        on_click=lambda e: ir_a("menu_principal"),
        content=ft.Image(src="logo_uniruta.png", height=42, fit="contain"),
    )

    info_usuario = ft.Row(
        spacing=12,
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.IconButton(
                icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                icon_color="#64748B",
                icon_size=22,
                tooltip="Notificaciones",
                on_click=abrir_notificaciones,
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
                    width=32,
                    height=32,
                    border=ft.Border.all(1, "#A0AEC0"),
                    border_radius=16,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#F1F5F9",
                    content=ft.Icon(
                        ft.Icons.PERSON_OUTLINE, size=18, color="#475569"
                    ),
                ),
                items=[
                    ft.PopupMenuItem(
                        icon=ft.Icons.PERSON_OUTLINE,
                        content=ft.Text("Mi Perfil", size=13),
                        on_click=lambda e: ir_a("perfil"),
                    ),
                    ft.PopupMenuItem(
                        icon=ft.Icons.SETTINGS_OUTLINED,
                        content=ft.Text("Configuración", size=13),
                        on_click=lambda e: ir_a("configuracion"),
                    ),
                    ft.PopupMenuItem(),  # Separador visual
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
        height=58,
        bgcolor="white",
        padding=ft.Padding(10, 0, 20, 0),
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[logo_header, info_usuario],
        ),
    )

    # --- 2. SIDEBAR LATERAL (AZUL TURQUESA) ---
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
                            ft.FontWeight.BOLD if activo else ft.FontWeight.W_500
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
                    "Menú principal",
                    ft.Icons.HOME_OUTLINED,
                    "menu_principal",
                    activo=True,
                ),
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes"),
                item_sidebar(
                    "Unidades", ft.Icons.DIRECTIONS_BUS_OUTLINED, "unidades"
                ),
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- 3. TARJETAS DE KPI (NARANJAS) ---
    def tarjeta_kpi(titulo, valor, subtitulo):
        return ft.Container(
            width=210,
            height=145,
            bgcolor="#EC932F",
            border=ft.Border.all(2.5, "#C87A22"),
            border_radius=14,
            padding=ft.Padding(15, 14, 15, 14),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=ft.Colors.with_opacity(0.15, "black"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        titulo,
                        color="white",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        str(valor),
                        color="white",
                        size=38,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        subtitulo,
                        color="white",
                        size=12,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        )

    kpi_unidades = tarjeta_kpi(
        "Unidades activas",
        resumen["unidades_activas"],
        f"de {resumen['total_unidades']} unidades",
    )
    kpi_choferes = tarjeta_kpi(
        "Choferes en turno",
        resumen["choferes_en_turno"],
        f"de {resumen['total_choferes']} disponibles",
    )
    kpi_viajes = tarjeta_kpi(
        "Viajes programados",
        resumen["viajes_programados"],
        f"Completados: {resumen['viajes_completados']}",
    )

    # --- 4. GRÁFICA DE BARRAS ---
    def crear_par_barras(h_azul, h_verde):
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=5,
            controls=[
                ft.Container(
                    width=15,
                    height=h_azul,
                    bgcolor="#3B92F6",
                    border_radius=ft.BorderRadius(3, 3, 0, 0),
                ),
                ft.Container(
                    width=15,
                    height=h_verde,
                    bgcolor="#10B981",
                    border_radius=ft.BorderRadius(3, 3, 0, 0),
                ),
            ],
        )

    grafica_barras = ft.Container(
        height=135,
        alignment=ft.Alignment(0, 1),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.END,
            controls=[
                crear_par_barras(60, 90),
                crear_par_barras(50, 100),
                crear_par_barras(75, 120),
            ],
        ),
    )

    seccion_desempeno = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Desempeño semanal de rutas",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color="#1E293B",
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Row([
                            ft.Container(
                                width=8,
                                height=8,
                                bgcolor="#3B92F6",
                                border_radius=4,
                            ),
                            ft.Text("Retrasos", size=10, color="#64748B"),
                        ]),
                        ft.Row([
                            ft.Container(
                                width=8,
                                height=8,
                                bgcolor="#10B981",
                                border_radius=4,
                            ),
                            ft.Text("Ganancias", size=10, color="#64748B"),
                        ]),
                    ],
                ),
                ft.Container(height=10),
                grafica_barras,
            ],
        ),
    )

    # --- 5. TABLA DE PRIORIDADES ---
    filas_prioridades = []
    datos_prioridades = (
        prioridades
        if prioridades
        else [
            ("Licencia por vencer/vencida", "Jaime Camil", "Vencido"),
            ("Unidad fuera de servicio", "ECO-006 (GHI-7890)", "Baja"),
            ("Unidad fuera de servicio", "ECO-947 (DHG-234)", "Mantenimiento"),
        ]
    )

    for idx, item in enumerate(datos_prioridades[:3]):
        tipo, entidad, estado = item
        bg_color = "#DDE2FF" if idx % 2 == 0 else "white"
        filas_prioridades.append(
            ft.DataRow(
                color=bg_color,
                cells=[
                    ft.DataCell(
                        ft.Text(str(tipo), size=11, color="#334155")
                    ),
                    ft.DataCell(
                        ft.Text(str(entidad), size=11, color="#334155")
                    ),
                    ft.DataCell(
                        ft.Text(str(estado), size=11, color="#334155")
                    ),
                ],
            )
        )

    tabla_prioridades = ft.DataTable(
        column_spacing=20,
        heading_row_height=28,
        data_row_min_height=32,
        columns=[
            ft.DataColumn(ft.Text("Tipo", size=11, color="#64748B")),
            ft.DataColumn(ft.Text("Unidad", size=11, color="#64748B")),
            ft.DataColumn(ft.Text("Estado", size=11, color="#64748B")),
        ],
        rows=filas_prioridades,
    )

    seccion_prioridades = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Prioridades",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color="#1E293B",
                ),
                ft.Container(height=10),
                tabla_prioridades,
            ],
        ),
    )

    # --- CÍRCULO AZUL GIGANTE DECORATIVO ---
    circulo_decorativo = ft.Container(
        width=320,
        height=320,
        bgcolor="#4298B8",
        border_radius=160,
        right=-80,
        top=-80,
    )

    # --- ÁREA DE CONTENIDO Y MAQUETACIÓN FINAL ---
    area_trabajo = ft.Stack(
        expand=True,
        controls=[
            ft.Container(expand=True, bgcolor="#FAFAFA"),
            circulo_decorativo,
            ft.Container(
                expand=True,
                padding=ft.Padding(25, 15, 25, 20),
                content=ft.Column(
                    spacing=22,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Menú principal",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color="#000000",
                                )
                            ],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=25,
                            controls=[kpi_unidades, kpi_choferes, kpi_viajes],
                        ),
                        ft.Container(height=10),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[seccion_desempeno, seccion_prioridades],
                        ),
                    ],
                ),
            ),
        ],
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