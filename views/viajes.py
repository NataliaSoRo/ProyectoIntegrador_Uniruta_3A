import flet as ft
from dao.viaje_dao import ViajeDAO
from models.viaje import Viaje
from dao.unidad_dao import UnidadDAO
from dao.chofer_dao import ChoferDAO
from dao.ruta_dao import RutaDAO


def vista_viajes(page: ft.Page, ir_a):
    page.title = "UniRuta - Viajes"

    # Instancia del DAO
    dao = ViajeDAO() if "ViajeDAO" in globals() else None
    unidad_dao = UnidadDAO()
    chofer_dao = ChoferDAO()
    ruta_dao = RutaDAO()

    # Usuario actual de la sesión (fallback a "Natalia Sosa Rodriguez" si no hay datos)
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = (
        getattr(usuario, "nombre", "Natalia Sosa Rodriguez")
        if usuario
        else "Natalia Sosa Rodriguez"
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
        # ✅ FORMA CORRECTA DE ABRIR DIÁLOGOS EN TU VERSIÓN DE FLET
        if dialogo not in page.overlay:
            page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

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
        # ✅ FORMA CORRECTA DE ABRIR DIÁLOGOS EN TU VERSIÓN DE FLET
        if dialogo_perfil not in page.overlay:
            page.overlay.append(dialogo_perfil)
        dialogo_perfil.open = True
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
                        on_click=abrir_perfil,  # ✅ Llama a la función que abre el cuadro flotante
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
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar(
                    "Viajes", ft.Icons.WORK_OUTLINE, "viajes", activo=True
                ),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- 3. TABLA ---
    tabla_viajes = ft.DataTable(
        bgcolor="white",
        heading_row_color="#EC932F",
        heading_row_height=38,
        data_row_min_height=52,
        column_spacing=20,
        columns=[
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
                    "No. Unidad",
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
                    "Ruta", color="white", size=11, weight=ft.FontWeight.BOLD
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Fecha", color="white", size=11, weight=ft.FontWeight.BOLD
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Hora de salida programada",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Estatus",
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

    #=============================
    # VARIABLE PARA SABER SI ESTAMOS EDITANDO
    #=============================
    id_viaje_edicion = None

    txt_titulo_modal = ft.Text(
        "Programar viaje",
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#0F172A",
    )

    txt_fecha_inner = ft.TextField(
        hint_text="AAAA-MM-DD",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )

    txt_fecha = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_fecha_inner,
    )

    txt_hora_inner = ft.TextField(
        hint_text="HH:MM",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )

    txt_hora = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_hora_inner,
    )

    txt_hora_llegada_inner = ft.TextField(
        hint_text="HH:MM",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )

    txt_hora_llegada = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_hora_llegada_inner,
    )

    txt_pasajeros_inner = ft.TextField(
        hint_text="Ej. 25",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )

    txt_pasajeros = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_pasajeros_inner,
    )

    txt_observaciones_inner = ft.TextField(
        hint_text="Escribe alguna observación...",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 8, 10, 8),
        text_size=12,
        multiline=True,
        min_lines=2,
        max_lines=3,
        expand=True,
    )

    txt_observaciones = ft.Container(
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        content=txt_observaciones_inner,
    )

    dd_estatus_inner = ft.Dropdown(
        hint_text="Seleccionar estatus",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        value="Programado",
        options=[
            ft.dropdown.Option("Programado"),
            ft.dropdown.Option("En curso"),
            ft.dropdown.Option("Concluido"),
            ft.dropdown.Option("Cancelado"),
        ],
        expand=True,
    )

    dd_estatus = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_estatus_inner,
    )

    dd_unidad_inner = ft.Dropdown(
        hint_text="Seleccionar unidad",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        options=[],
        expand=True,
    )

    dd_chofer_inner = ft.Dropdown(
        hint_text="Seleccionar chofer",
        options=[],
        expand=True,
    )

    dd_chofer = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        content=dd_chofer_inner,
    )

    dd_ruta_inner = ft.Dropdown(
        hint_text="Seleccionar ruta",
        options=[],
        expand=True,
    )

    dd_ruta = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        content=dd_ruta_inner,
    )

    def cargar_dropdowns():

        # UNIDADES
        dd_unidad_inner.options = [
            ft.dropdown.Option(
                key=str(u.id),
                text=u.noeconomico
            )
            for u in unidad_dao.obtener_todos()
        ]

        # CHOFERES
        dd_chofer_inner.options = [
            ft.dropdown.Option(
                key=str(c.id),
                text=c.nombre
            )
            for c in chofer_dao.obtener_todos()
        ]

        # RUTAS
        dd_ruta_inner.options = [
            ft.dropdown.Option(
                key=str(r.id),
                text=r.nombre
            )
            for r in ruta_dao.obtener_todos()
        ]

    dd_unidad = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_unidad_inner,
    )
    
    def guardar_viaje(e):

        ruta_dao = RutaDAO()

        rutas = ruta_dao.obtener_todos()

        origen = ""
        destino = ""

        for ruta in rutas:
            if str(ruta.id) == str(dd_ruta_inner.value):
                origen = ruta.origen
                destino = ruta.destino
                break

        viaje = Viaje(
            fecha=txt_fecha_inner.value,
            hora=txt_hora_inner.value,
            hora_llegada=txt_hora_llegada_inner.value,
            pasajeros=txt_pasajeros_inner.value,
            observaciones=txt_observaciones_inner.value,
            id_unidad=dd_unidad_inner.value,
            id_chofer=dd_chofer_inner.value,
            id_ruta=dd_ruta_inner.value,
            estatus=dd_estatus_inner.value,
        )

        viaje.origen = origen
        viaje.destino = destino

        print("Ruta seleccionada:", dd_ruta_inner.value)
        print("Origen:", origen)
        print("Destino:", destino)

        dao.insertar(viaje)

        modal_programar.open = False
        cargar_datos_tabla()
        page.update()
    
    def abrir_modal_programar(e):

        cargar_dropdowns()

        txt_titulo_modal.value = "Programar viaje"

        if modal_programar not in page.overlay:
            page.overlay.append(modal_programar)

        modal_programar.open = True
        page.update()

    def eliminar_viaje(id_v):
        if dao and hasattr(dao, "eliminar"):
            dao.eliminar(id_v)
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
        for v in lista:
            # 1. ID Viaje
            id_v = getattr(v, "id", "V-000")
            id_viaje = str(id_v)

            # 2. No. Unidad
            unidad = getattr(v, "id_unidad", "-")

            # 3. Chofer asignado
            chofer = getattr(v, "chofer_nombre", "Sin asignar") or "Sin asignar"

            # 4. Nombre de la Ruta (Prioriza ruta_nombre sobre origen/destino e ID)
            if getattr(v, "ruta_nombre", None):
                ruta_display = v.ruta_nombre
            elif getattr(v, "origen", None) and getattr(v, "destino", None):
                ruta_display = f"{v.origen} - {v.destino}"
            else:
                ruta_display = "-"

            # 5. Fecha
            fecha = str(getattr(v, "fecha", "-"))

            # 6. Hora
            hora = str(getattr(v, "hora", "00:00"))

            # 7. Estatus y Colores
            estatus = str(getattr(v, "estatus", "Inactivo")).capitalize()
            estatus_lower = estatus.lower()

            if "curso" in estatus_lower or "programado" in estatus_lower:
                color_estatus = "#10B981"  # Verde
            elif "concluido" in estatus_lower or "finalizado" in estatus_lower:
                color_estatus = "#EC932F"  # Naranja
            else:
                color_estatus = "#64748B"  # Gris

            # Construcción de la fila de la tabla
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                id_viaje,
                                size=11,
                                color="#1E293B",
                                weight=ft.FontWeight.W_500,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(str(unidad), size=11, color="#1E293B")
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Icon(
                                            ft.Icons.PERSON,
                                            size=13,
                                            color="white",
                                        ),
                                        bgcolor="#94A3B8",
                                        radius=11,
                                    ),
                                    ft.Text(
                                        str(chofer),
                                        size=11,
                                        color="#1E293B",
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ],
                                spacing=6,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(str(ruta_display), size=11, color="#1E293B")
                        ),
                        ft.DataCell(
                            ft.Container(
                                padding=ft.Padding(6, 3, 6, 3),
                                border=ft.Border.all(1, "#CBD5E1"),
                                border_radius=4,
                                content=ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.CALENDAR_TODAY_OUTLINED,
                                            size=12,
                                            color="#0284C7",
                                        ),
                                        ft.Text(
                                            fecha, size=10, color="#1E293B"
                                        ),
                                    ],
                                    spacing=4,
                                    tight=True,
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                padding=ft.Padding(12, 3, 12, 3),
                                border=ft.Border.all(1, "#CBD5E1"),
                                border_radius=12,
                                content=ft.Text(
                                    hora, size=11, color="#1E293B"
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                estatus,
                                size=11,
                                color=color_estatus,
                                weight=ft.FontWeight.BOLD,
                            )
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
                                        on_click=lambda e, viaje=v: editar_viaje(viaje),
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
                                        uid=id_v: eliminar_viaje(uid),
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
        tabla_viajes.rows = filas

    def al_cambiar_buscador(e):
        cargar_datos_tabla(e.control.value)
        page.update()

    # --- 4. CONTROLES Y BUSCADOR ---
    buscador = ft.TextField(
        hint_text="Busca chofer",
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

    modal_programar = ft.AlertDialog(
        content=ft.Container(
            width=550,
            padding=20,
            bgcolor="white",
            border_radius=12,
            content=ft.Column(
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    txt_titulo_modal,

                    ft.Text("Fecha"),
                    txt_fecha,

                    ft.Text("Hora de salida"),
                    txt_hora,

                    ft.Text("Hora de llegada"),
                    txt_hora_llegada,

                    ft.Text("Pasajeros"),
                    txt_pasajeros,

                    ft.Text("Unidad"),
                    dd_unidad,

                    ft.Text("Chofer"),
                    dd_chofer,

                    ft.Text("Ruta"),
                    dd_ruta,

                    ft.Text("Estatus"),
                    dd_estatus,

                    ft.Text("Observaciones"),
                    txt_observaciones,

                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Guardar",
                                bgcolor="#6366F1",
                                color="white",
                                expand=True,
                                on_click=guardar_viaje
                            ),

                            ft.ElevatedButton(
                                "Cancelar",
                                bgcolor="#F97316",
                                color="white",
                                expand=True,
                                on_click=lambda e: (
                                    setattr(modal_programar, "open", False),
                                    page.update(),
                                ),
                            ),
                        ]
                    ),
                ],
            ),
        )
    )

    btn_programar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ADD, color="white", size=16),
                ft.Text(
                    "Programar viaje",
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
        on_click=abrir_modal_programar 
    )

    def editar_viaje(viaje):
    
        global id_viaje_edicion

        id_viaje_edicion = viaje.id

        txt_titulo_modal.value = "Editar viaje"

        txt_fecha_inner.value = str(viaje.fecha)
        txt_hora_inner.value = str(viaje.hora)
        txt_hora_llegada_inner.value = str(viaje.hora_llegada)
        txt_pasajeros_inner.value = str(viaje.pasajeros)
        txt_observaciones_inner.value = str(viaje.observaciones)

        dd_unidad_inner.value = str(viaje.id_unidad)
        dd_chofer_inner.value = str(viaje.id_chofer)
        dd_ruta_inner.value = str(viaje.id_ruta)
        dd_estatus_inner.value = str(viaje.estatus)

        if modal_programar not in page.overlay:
            page.overlay.append(modal_programar)

        modal_programar.open = True
        page.update()

    barra_controles = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[ft.Container(width=420, content=buscador), btn_programar],
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
        content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[tabla_viajes]),
    )

    # --- ÁREA DE TRABAJO ---
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
                    "Viajes",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                barra_controles,
                contenedor_tabla,
            ],
        ),
    )

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            header,
            ft.Row(expand=True, spacing=0, controls=[sidebar, area_trabajo]),
        ],
    )