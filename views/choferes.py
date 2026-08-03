import flet as ft
from datetime import datetime

try:
    from dao.chofer_dao import ChoferDAO
except ImportError:
    ChoferDAO = None


def vista_choferes(page: ft.Page, ir_a):
    page.title = "UniRuta - Choferes"

    dao = ChoferDAO() if ChoferDAO else None

    # Usuario actual de la sesión
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = (
        getattr(usuario, "nombre", "Juana Suarez") if usuario else "Juana Suarez"
    )
    rol_usuario = (
        getattr(usuario, "rol", "Administrador") if usuario else "Administrador"
    )

    # --- INICIALIZACIÓN DE SERVICIOS (FilePicker y DatePicker) ---
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    ruta_imagen_seleccionada = {"path": None}

    def al_seleccionar_archivo(e):
        if e.files and len(e.files) > 0:
            ruta = e.files[0].path
            ruta_imagen_seleccionada["path"] = ruta
            contenedor_foto.content = ft.Image(
                src=ruta,
                fit=ft.BoxFit.COVER,
                border_radius=ft.border_radius.all(8),
            )
            contenedor_foto.update()

    file_picker.on_result = al_seleccionar_archivo

    # Calendar DatePicker para vigencia
    def al_cambiar_fecha(e):
        if date_picker.value:
            txt_vigencia.value = date_picker.value.strftime("%Y-%m-%d")
            txt_vigencia.update()

    date_picker = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2040, 12, 31),
        on_change=al_cambiar_fecha,
    )

    def abrir_calendario(e):
        if date_picker not in page.overlay:
            page.overlay.append(date_picker)
        date_picker.open = True
        page.update()

    # --- LÓGICA DE CERRAR SESIÓN Y NOTIFICACIONES ---
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
                        subtitle=ft.Text("Revisa la vigencia de los choferes.", size=11),
                    ),
                ],
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo))
            ],
        )
        if dialogo not in page.overlay:
            page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    # --- BARRA SUPERIOR (HEADER) ---
    logo_header = ft.Container(
        padding=ft.Padding(10, 0, 0, 0),
        on_click=lambda e: ir_a("menu_principal"),
        content=ft.Image(src="logo_uniruta.png", height=38, fit=ft.BoxFit.CONTAIN),
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
                        content=ft.Text("1", size=9, color="white", weight=ft.FontWeight.BOLD),
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
                    ft.Text(nombre_usuario, size=12, weight=ft.FontWeight.BOLD, color="#1E293B"),
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
                    content=ft.Icon(ft.Icons.PERSON_OUTLINE, size=18, color="#475569"),
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
            color="#0D000000",
            offset=ft.Offset(0, 2),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[logo_header, info_usuario],
        ),
    )

    # --- SIDEBAR LATERAL ---
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
                        weight=(ft.FontWeight.BOLD if activo else ft.FontWeight.W_500),
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
                    content=ft.IconButton(icon=ft.Icons.MENU, icon_color="#1E293B"),
                ),
                item_sidebar("Menú principal", ft.Icons.HOME_OUTLINED, "menu_principal"),
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes", activo=True),
                item_sidebar("Unidades", ft.Icons.DIRECTIONS_BUS_OUTLINED, "unidades"),
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- TABLA Y DATOS ---
    tabla_choferes = ft.DataTable(
        bgcolor="white",
        heading_row_color="#EC932F",
        heading_row_height=38,
        data_row_min_height=48,
        column_spacing=16,
        columns=[
            ft.DataColumn(ft.Text("NO.", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre del chofer", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Teléfono", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("No. Licencia", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo de licencia", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Vigencia de licencia", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color="white", size=11, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def eliminar_chofer(id_chofer):
        if dao and hasattr(dao, "eliminar") and dao.eliminar(id_chofer):
            cargar_datos_tabla()
            page.update()

    def obtener_valor(item, clave, valor_defecto="-"):
        if isinstance(item, dict):
            return item.get(clave) or valor_defecto
        return getattr(item, clave, None) or valor_defecto

    def cargar_datos_tabla(filtro=""):
        lista = []
        if dao:
            if filtro.strip() and hasattr(dao, "buscar_por_nombre"):
                lista = dao.buscar_por_nombre(filtro)
            elif hasattr(dao, "obtener_todos"):
                lista = dao.obtener_todos()

        filas = []
        for idx, c in enumerate(lista, start=1):
            id_ch = obtener_valor(c, "id", None)
            nombre_ch = obtener_valor(c, "nombre", "")
            telefono_ch = obtener_valor(c, "telefono", "-")
            licencia_ch = obtener_valor(c, "licencia", "-")
            tipo_lic_ch = obtener_valor(c, "tipo_licencia", "-")
            vigen_lic_ch = obtener_valor(c, "vigen_licencia", "-")
            estatus_str = str(obtener_valor(c, "estatus", "Inactivo"))

            if estatus_str.lower() in ["activo", "disponible"]:
                color_est = "#10B981"
            elif estatus_str.lower() in ["vencido"]:
                color_est = "#EF4444"
            else:
                color_est = "#F59E0B"

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idx), size=11, color="#1E293B")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Icon(ft.Icons.PERSON, size=14, color="white"),
                                        bgcolor="#94A3B8",
                                        radius=12,
                                    ),
                                    ft.Text(
                                        str(nombre_ch),
                                        size=11,
                                        color="#1E293B",
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ],
                                spacing=8,
                            )
                        ),
                        ft.DataCell(ft.Text(str(telefono_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(licencia_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(tipo_lic_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(vigen_lic_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(estatus_str, size=11, color=color_est, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#0284C7"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=lambda e, i=id_ch: print(f"Editar {i}"),
                                        content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=13, color="#0284C7"),
                                    ),
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#EF4444"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        on_click=lambda e, i=id_ch: eliminar_chofer(i),
                                        content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=13, color="#EF4444"),
                                    ),
                                ],
                                spacing=6,
                            )
                        ),
                    ]
                )
            )
        tabla_choferes.rows = filas

    def al_cambiar_buscador(e):
        cargar_datos_tabla(e.control.value)
        page.update()

    # --- CONTROLES DEL FORMULARIO DE REGISTRO ---
    def seleccionar_imagen(e):
        file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    contenedor_foto = ft.Container(
        height=135,
        bgcolor="#E2E8F0",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=seleccionar_imagen,
        tooltip="Haga clic para subir una imagen",
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Icon(ft.Icons.ADD_A_PHOTO_OUTLINED, size=32, color="#64748B"),
                ft.Text("Subir foto", size=10, color="#64748B", weight=ft.FontWeight.W_500)
            ]
        )
    )

    txt_nombre = ft.TextField(
        hint_text="ej. Juan Lopez",
        height=38,
        content_padding=ft.Padding(10, 0, 10, 0),
        border_radius=8,
        bgcolor="#F8FAFC",
        border_color="#CBD5E1",
        text_size=12,
    )

    # DESPLEGABLE (Dropdown)
    dd_tipo_licencia = ft.Dropdown(
        hint_text="Seleccionar tipo",
        height=38,
        content_padding=ft.Padding(10, 0, 10, 0),
        border_radius=8,
        bgcolor="#F8FAFC",
        border_color="#CBD5E1",
        text_size=12,
        options=[
            ft.dropdown.Option("Estatal tipo A"),
            ft.dropdown.Option("Estatal tipo B"),
            ft.dropdown.Option("Federal tipo A"),
            ft.dropdown.Option("Federal tipo B"),
        ],
    )

    # CAMPO DE FECHA
    txt_vigencia = ft.TextField(
        hint_text="AAAA-MM-DD",
        height=38,
        content_padding=ft.Padding(10, 0, 10, 0),
        border_radius=8,
        bgcolor="#F8FAFC",
        border_color="#CBD5E1",
        text_size=12,
        read_only=True,
        suffix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_calendario,
    )

    txt_telefono = ft.TextField(
        hint_text="+52 ej. 246 365 8385",
        height=38,
        content_padding=ft.Padding(10, 0, 10, 0),
        border_radius=8,
        bgcolor="#F8FAFC",
        border_color="#CBD5E1",
        text_size=12,
    )

    txt_no_licencia = ft.TextField(
        hint_text="ej. A-1234",
        height=38,
        content_padding=ft.Padding(10, 0, 10, 0),
        border_radius=8,
        bgcolor="#F8FAFC",
        border_color="#CBD5E1",
        text_size=12,
    )

    def restablecer_formulario():
        txt_nombre.value = ""
        dd_tipo_licencia.value = None
        txt_vigencia.value = ""
        txt_telefono.value = ""
        txt_no_licencia.value = ""
        ruta_imagen_seleccionada["path"] = None
        contenedor_foto.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Icon(ft.Icons.ADD_A_PHOTO_OUTLINED, size=32, color="#64748B"),
                ft.Text("Subir foto", size=10, color="#64748B", weight=ft.FontWeight.W_500)
            ]
        )

    def guardar_chofer(e):
        datos_chofer = {
            "nombre": txt_nombre.value,
            "telefono": txt_telefono.value,
            "licencia": txt_no_licencia.value,
            "tipo_licencia": dd_tipo_licencia.value,
            "vigen_licencia": txt_vigencia.value,
            "foto": ruta_imagen_seleccionada["path"],
            "estatus": "Activo",
        }

        if dao:
            try:
                if hasattr(dao, "insertar"):
                    dao.insertar(datos_chofer)
                elif hasattr(dao, "guardar"):
                    dao.guardar(datos_chofer)
                elif hasattr(dao, "crear"):
                    dao.crear(datos_chofer)
            except Exception as ex:
                print(f"Error al guardar: {ex}")

        restablecer_formulario()
        modal_agregar.open = False
        cargar_datos_tabla()

        # MOSTRAR NOTIFICACIÓN (SnackBar)
        snack = ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="white"),
                    ft.Text("Chofer registrado correctamente", color="white", weight=ft.FontWeight.BOLD)
                ]
            ),
            bgcolor="#10B981",
            duration=3000,
        )
        page.overlay.append(snack)
        snack.open = True

        page.update()

    def cancelar_modal(e):
        restablecer_formulario()
        modal_agregar.open = False
        page.update()

    modal_content = ft.Container(
        width=520,
        padding=ft.Padding(20, 15, 20, 20),
        bgcolor="white",
        border_radius=12,
        content=ft.Stack(
            controls=[
                ft.Container(
                    top=0,
                    right=0,
                    content=ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color="#1E293B",
                        icon_size=20,
                        on_click=cancelar_modal,
                    ),
                ),
                ft.Column(
                    tight=True,
                    spacing=15,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(0, 10, 0, 5),
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text(
                                "Agregar chofer",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color="#0F172A",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ),
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            spacing=20,
                            controls=[
                                ft.Column(
                                    expand=1,
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.START,
                                    controls=[
                                        ft.Text("Imagen del conductor", size=11, color="#475569", weight=ft.FontWeight.W_600),
                                        contenedor_foto,
                                        ft.Text("No. licencia", size=11, color="#475569", weight=ft.FontWeight.W_600),
                                        txt_no_licencia,
                                    ],
                                ),
                                ft.Column(
                                    expand=1,
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.START,
                                    controls=[
                                        ft.Text("Nombre completo", size=11, color="#475569", weight=ft.FontWeight.W_600),
                                        txt_nombre,
                                        ft.Text("Tipo de licencia", size=11, color="#475569", weight=ft.FontWeight.W_600),
                                        dd_tipo_licencia,
                                        ft.Text("Vigencia de licencia", size=11, color="#475569", weight=ft.FontWeight.W_600),
                                        txt_vigencia,
                                        ft.Text("Numero telefonico", size=11, color="#475569", weight=ft.FontWeight.W_600),
                                        txt_telefono,
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(height=5),
                        ft.Row(
                            spacing=15,
                            controls=[
                                ft.ElevatedButton(
                                    "Aceptar",
                                    bgcolor="#6366F1",
                                    color="white",
                                    expand=True,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.Padding(0, 14, 0, 14),
                                    ),
                                    on_click=guardar_chofer,
                                ),
                                ft.ElevatedButton(
                                    "Cancelar",
                                    bgcolor="#F97316",
                                    color="white",
                                    expand=True,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.Padding(0, 14, 0, 14),
                                    ),
                                    on_click=cancelar_modal,
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),
    )

    modal_agregar = ft.AlertDialog(
        content=modal_content,
        bgcolor="white",
        shape=ft.RoundedRectangleBorder(radius=12),
        content_padding=0,
    )

    def abrir_modal_agregar(e):
        if modal_agregar not in page.overlay:
            page.overlay.append(modal_agregar)
        modal_agregar.open = True
        page.update()

    # --- BUSCADOR Y BOTÓN ---
    buscador = ft.TextField(
        hint_text="Search",
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

    btn_ingresar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ADD, color="white", size=16),
                ft.Text(
                    "Ingresar chofer",
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
        on_click=abrir_modal_agregar,
    )

    barra_controles = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[ft.Container(width=380, content=buscador), btn_ingresar],
    )

    cargar_datos_tabla()

    contenedor_tabla = ft.Container(
        bgcolor="white",
        border_radius=8,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color="#1A000000",
            offset=ft.Offset(0, 3),
        ),
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO, controls=[tabla_choferes]
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
                    "Choferes",
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
                controls=[sidebar, area_trabajo],
            ),
        ],
    )