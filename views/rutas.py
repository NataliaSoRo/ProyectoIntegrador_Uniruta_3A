import flet as ft
from dao.ruta_dao import RutaDAO


def vista_rutas(page: ft.Page, ir_a):
    page.title = "UniRuta - Rutas"

    # Instancia del DAO
    dao = RutaDAO()

    # Usuario actual de la sesión (fallback a "Juana Suarez" si no hay datos)
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = (
        getattr(usuario, "nombre", "Juana Suarez") if usuario else "Juana Suarez"
    )
    rol_usuario = (
        getattr(usuario, "rol", "Administrador") if usuario else "Administrador"
    )
    correo_usuario = (
        getattr(
            usuario, "correo", getattr(usuario, "email", "usuario@uniruta.com")
        )
        if usuario
        else "usuario@uniruta.com"
    )

    # --- LÓGICA DE DIÁLOGOS (HEADER) ---
    def cerrar_sesion(e):
        if hasattr(page, "usuario_actual"):
            page.usuario_actual = None
        ir_a("login")

    def abrir_notificaciones(e):
        dialogo = ft.AlertDialog(
            title=ft.Text("Notificaciones", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.BADGE_OUTLINED, color="#3B82F6"
                        ),
                        title=ft.Text("Licencia por vencer", size=13),
                        subtitle=ft.Text(
                            "Revisa la vigencia de los choferes.", size=11
                        ),
                    ),
                ],
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.close(dialogo))
            ],
        )
        page.open(dialogo)

    def abrir_perfil(e):
        dialogo_perfil = ft.AlertDialog(
            title=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="#0E4A5B", size=28),
                    ft.Text(
                        "Mi Perfil",
                        weight=ft.FontWeight.BOLD,
                        size=18,
                        color="#0F172A",
                    ),
                ],
            ),
            content=ft.Container(
                width=320,
                padding=ft.Padding(10, 10, 10, 10),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Icon(
                                ft.Icons.PERSON, size=36, color="white"
                            ),
                            bgcolor="#0E4A5B",
                            radius=32,
                        ),
                        ft.Text(
                            nombre_usuario,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                        ),
                        ft.Container(
                            bgcolor="#E0F2FE",
                            border_radius=12,
                            padding=ft.Padding(10, 4, 10, 4),
                            content=ft.Text(
                                rol_usuario,
                                size=11,
                                color="#0369A1",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                        ft.Divider(height=1, color="#E2E8F0"),
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.EMAIL_OUTLINED,
                                    size=16,
                                    color="#64748B",
                                ),
                                ft.Text(
                                    correo_usuario, size=12, color="#334155"
                                ),
                            ]
                        ),
                    ],
                ),
            ),
            actions=[
                ft.TextButton(
                    "Cerrar", on_click=lambda e: page.close(dialogo_perfil)
                )
            ],
        )
        page.open(dialogo_perfil)

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
                        on_click=abrir_perfil,
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
                ),
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes"),
                item_sidebar(
                    "Unidades", ft.Icons.DIRECTIONS_BUS_OUTLINED, "unidades"
                ),
                item_sidebar(
                    "Rutas", ft.Icons.MAP_OUTLINED, "rutas", activo=True
                ),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- 3. TABLA Y DATOS DINÁMICOS ---
    tabla_rutas = ft.DataTable(
        bgcolor="white",
        heading_row_color="#EC932F",
        heading_row_height=38,
        data_row_min_height=48,
        column_spacing=24,
        columns=[
            ft.DataColumn(
                ft.Text(
                    "ID de la ruta",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Nombre de la ruta",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Origen",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Destino",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Tiempo estimado",
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

    def obtener_val(r, llaves, por_defecto=""):
        for llave in llaves:
            if isinstance(r, dict) and llave in r and r[llave] is not None:
                return r[llave]
            if hasattr(r, llave) and getattr(r, llave) is not None:
                return getattr(r, llave)
        return por_defecto

    def eliminar_ruta(id_r):
        if hasattr(dao, "eliminar") and dao.eliminar(id_r):
            cargar_datos_tabla()
            page.update()

    def cargar_datos_tabla(filtro=""):
        lista = []
        if filtro.strip():
            if hasattr(dao, "buscar"):
                lista = dao.buscar(filtro)
            elif hasattr(dao, "buscar_por_nombre"):
                lista = dao.buscar_por_nombre(filtro)
        else:
            if hasattr(dao, "obtener_todas"):
                lista = dao.obtener_todas()
            elif hasattr(dao, "obtener_todos"):
                lista = dao.obtener_todos()

        # Datos de prueba si no viene nada de BD
        if not lista:
            lista = [
                {
                    "ID": 1,
                    "Nombre de la ruta": "Huamantla - Apizaco",
                    "Origen": "Huamantla",
                    "Destino": "UTT",
                    "Tiempo estimado": "00:15:00",
                },
                {
                    "ID": 2,
                    "Nombre de la ruta": "Terrenate - Huamantla",
                    "Origen": "Terrenate",
                    "Destino": "UTT",
                    "Tiempo estimado": "00:20:00",
                },
                {
                    "ID": 3,
                    "Nombre de la ruta": "H. Galeana - Huamantla",
                    "Origen": "Galeana",
                    "Destino": "UTT",
                    "Tiempo estimado": "00:25:00",
                },
                {
                    "ID": 4,
                    "Nombre de la ruta": "Apizaco - Xalpatlahuaya",
                    "Origen": "Apizaco",
                    "Destino": "UTT",
                    "Tiempo estimado": "00:45:00",
                },
            ]

        filas = []
        for idx, r in enumerate(lista, start=1):
            id_r = obtener_val(r, ["ID", "id", "id_ruta"], idx)
            nombre = obtener_val(
                r,
                ["Nombre de la ruta", "nombre", "nombre_ruta", "Nombre"],
                "Sin Nombre",
            )
            origen = obtener_val(r, ["Origen", "origen"], "S/N")
            destino = obtener_val(r, ["Destino", "destino"], "S/N")
            tiempo = obtener_val(
                r,
                ["Tiempo estimado", "tiempo_estimado", "tiempo"],
                "00:00:00",
            )

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(id_r),
                                size=11,
                                color="#1E293B",
                                weight=ft.FontWeight.W_500,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(nombre),
                                size=11,
                                color="#1E293B",
                                weight=ft.FontWeight.W_500,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(str(origen), size=11, color="#475569")
                        ),
                        ft.DataCell(
                            ft.Text(str(destino), size=11, color="#475569")
                        ),
                        ft.DataCell(
                            ft.Text(str(tiempo), size=11, color="#475569")
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#EC932F"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=lambda e,
                                        uid=id_r: print(f"Editar {uid}"),
                                        content=ft.Icon(
                                            ft.Icons.EDIT_OUTLINED,
                                            size=13,
                                            color="#EC932F",
                                        ),
                                    ),
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#EF4444"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=lambda e,
                                        uid=id_r: eliminar_ruta(uid),
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
        tabla_rutas.rows = filas

    def al_cambiar_buscador(e):
        cargar_datos_tabla(e.control.value)
        page.update()

    # --- 4. BUSCADOR Y BOTÓN ---
    buscador = ft.TextField(
        hint_text="Buscar ruta",
        prefix_icon=ft.Icons.SEARCH,
        height=36,
        content_padding=ft.Padding(12, 0, 12, 0),
        border_radius=18,
        bgcolor="white",
        border_color="#CBD5E1",
        focused_border_color="#EC932F",
        text_size=12,
        on_change=al_cambiar_buscador,
    )

    btn_agregar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ADD, color="white", size=16),
                ft.Text(
                    "Agregar ruta",
                    color="white",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=4,
        ),
        bgcolor="#EC932F",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=18),
            padding=ft.Padding(16, 6, 16, 6),
        ),
        on_click=lambda e: print("Abrir modal ruta"),
    )

    barra_controles = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Container(width=380, content=buscador),
            btn_agregar,
        ],
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
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[tabla_rutas],
        ),
    )

    # --- ÁREA DE CONTENIDO FINAL ---
    area_trabajo = ft.Container(
        expand=True,
        bgcolor="#FAFAFA",
        padding=ft.Padding(25, 15, 25, 20),
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Rutas",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                barra_controles,
                contenedor_tabla,
            ],
        ),
    )

    # --- ESTRUCTURA GENERAL ---
    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            header,
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,
                    area_trabajo,
                ],
            ),
        ],
    )