import flet as ft
from dao.unidad_dao import UnidadDAO
from models.unidad import Unidad


def vista_unidades(page: ft.Page, ir_a):
    page.title = "UniRuta - Unidades"

    dao = UnidadDAO()

    id_unidad_edicion = None

    # Usuario actual de la sesión
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
        def cerrar_dialogo(e):
            dialogo.open = False
            page.update()

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
            actions=[ft.TextButton("Cerrar", on_click=cerrar_dialogo)],
        )
        if dialogo not in page.overlay:
            page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def abrir_perfil(e):
        def cerrar_perfil(e):
            dialogo_perfil.open = False
            page.update()

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
            actions=[ft.TextButton("Cerrar", on_click=cerrar_perfil)],
        )
        if dialogo_perfil not in page.overlay:
            page.overlay.append(dialogo_perfil)
        dialogo_perfil.open = True
        page.update()

    # --- 1. BARRA SUPERIOR (HEADER) ---
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
                    "Menú principal", ft.Icons.HOME_OUTLINED, "menu_principal"
                ),
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes"),
                item_sidebar(
                    "Unidades",
                    ft.Icons.DIRECTIONS_BUS_OUTLINED,
                    "unidades",
                    activo=True,
                ),
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- 3. EXTRACCIÓN Y MAQUETADO DE TARJETAS ---
    def obtener_val(u, llaves, por_defecto="S/N"):
        for llave in llaves:
            if isinstance(u, dict) and llave in u and u[llave] is not None:
                return u[llave]
            if hasattr(u, llave) and getattr(u, llave) is not None:
                return getattr(u, llave)
        return por_defecto

    carrusel_listview = ft.ListView(
        expand=True,
        horizontal=True,
        spacing=20,
        padding=ft.Padding(10, 15, 10, 15),
    )

    def eliminar_unidad(id_unidad):
        if hasattr(dao, "eliminar") and dao.eliminar(id_unidad):
            cargar_unidades()
            page.update()

    def confirmar_eliminacion(id_unidad):
        def cancelar(e):
            dialogo.open = False
            page.update()

        def confirmar(e):
            eliminar_unidad(id_unidad)
            dialogo.open = False
            cargar_unidades()
            page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar unidad"),
            content=ft.Text("¿Estás seguro de eliminar esta unidad?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton(
                    "Eliminar", 
                    bgcolor="RED",
                    color="white",
                    on_click=confirmar,
                ),
            ],
        )

        if dialogo not in page.overlay:
            page.overlay.append(dialogo)

        dialogo.open = True
        page.update()

    def crear_tarjeta_unidad(u, indice=0):
        id_u = obtener_val(u, ["id", "ID", "id_unidad"], None)

        no_economico = obtener_val(
            u,
            [
                "noeconomico",
                "No. Economico",
                "No_economico",
                "numero_economico",
                "num_economico",
            ],
            f"ECO-{900 + indice}",
        )

        val_modelo = obtener_val(
            u, ["modelo", "Modelo", "nombre_modelo"], "Sin especificar"
        )
        placas = obtener_val(u, ["placas", "Placas"], "S/N")
        estatus = obtener_val(u, ["estatus", "Estatus", "estado"], "Inactivo")

        img_db = obtener_val(u, ["imagen", "foto", "Imagen"], None)
        if img_db:
            str_img = str(img_db).strip()
            img_src = str_img if ("." in str_img) else f"{str_img}.png"
        else:
            num_combi = (indice % 3) + 1
            img_src = f"combi_{num_combi}.png"

        return ft.Container(
            width=220,
            bgcolor="white",
            border_radius=12,
            padding=ft.Padding(14, 14, 14, 16),
            shadow=ft.BoxShadow(
                blur_radius=12,
                color=ft.Colors.with_opacity(0.12, "black"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        height=95,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Image(
                            src=img_src,
                            fit="contain",
                            error_content=ft.Icon(
                                ft.Icons.DIRECTIONS_BUS,
                                size=50,
                                color="#64748B",
                            ),
                        ),
                    ),
                    ft.Text(
                        str(no_economico),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#0F172A",
                    ),
                    ft.Text(
                        f"Modelo: {val_modelo}",
                        size=11,
                        color="#475569",
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(f"Placas: {placas}", size=10, color="#475569"),
                    ft.Text(f"Estatus: {estatus}", size=10, color="#475569"),
                    ft.Container(height=6),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Text(
                                    "Editar",
                                    color="white",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                bgcolor="#5B65F5",
                                style=ft.ButtonStyle(
                                    padding=ft.Padding(10, 6, 10, 6),
                                    shape=ft.RoundedRectangleBorder(radius=6),
                                ),
                                on_click=lambda e, unidad=u: editar_unidad(unidad)
                            ),
                            ft.Container(
                                width=32,
                                height=32,
                                bgcolor="#1E1B4B",
                                border_radius=16,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, uid=id_u: confirmar_eliminacion(
                                    uid
                                ),
                                content=ft.Icon(
                                    ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    size=16,
                                    color="white",
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def cargar_unidades(filtro=""):
        lista = []
        if filtro.strip():
            if hasattr(dao, "buscar_por_codigo"):
                lista = dao.buscar_por_codigo(filtro)
            elif hasattr(dao, "buscar"):
                lista = dao.buscar(filtro)
        else:
            if hasattr(dao, "obtener_todos"):
                lista = dao.obtener_todos()

        if not lista:
            lista = [
                {
                    "id": 1,
                    "noeconomico": "ECO-947",
                    "modelo": "Sprinter",
                    "placas": "DHG-234",
                    "estatus": "Mantenimiento",
                    "imagen": "combi_1.png",
                },
                {
                    "id": 2,
                    "noeconomico": "ECO-102",
                    "modelo": "Urvan",
                    "placas": "ABC-123",
                    "estatus": "Activo",
                    "imagen": "combi_2.png",
                },
                {
                    "id": 3,
                    "noeconomico": "ECO-103",
                    "modelo": "Hiace",
                    "placas": "XYZ-567",
                    "estatus": "Activo",
                    "imagen": "combi_3.png",
                },
            ]

        carrusel_listview.controls = [
            crear_tarjeta_unidad(u, idx) for idx, u in enumerate(lista)
        ]

    def al_cambiar_buscador(e):
        cargar_unidades(e.control.value)
        page.update()

    # --- FORMULARIO Y MODAL AGREGAR UNIDAD ---

    # ID de la unidad que estamos editando
    id_unidad_edicion = None

    txt_economico = ft.TextField(
        label="No. Económico", hint_text="Ej. ECO-001", height=48, text_size=12
    )
    txt_placas = ft.TextField(
        label="Placas", hint_text="Ej. ABC-123", height=48, text_size=12
    )
    txt_modelo = ft.TextField(
        label="Modelo", hint_text="Ej. Sprinter", height=48, text_size=12
    )
    txt_marca = ft.TextField(
        label="Marca", hint_text="Ej. Mercedes", height=48, text_size=12
    )
    txt_anio = ft.TextField(
        label="Año", hint_text="Ej. 2022", height=48, text_size=12
    )
    txt_kilometraje = ft.TextField(
        label="Kilometraje", hint_text="Ej. 50000", height=48, text_size=12
    )
    lbl_error = ft.Text("", color="red", size=11)

    def limpiar_formulario():
        txt_economico.value = ""
        txt_placas.value = ""
        txt_modelo.value = ""
        txt_marca.value = ""
        txt_anio.value = ""
        txt_kilometraje.value = ""
        lbl_error.value = ""

    def cerrar_modal_agregar(e):
        modal_agregar.open = False
        page.update()

    def guardar_unidad(e):
        try:
            anio_val = int(txt_anio.value) if txt_anio.value.isdigit() else 0
            km_val = (
                int(txt_kilometraje.value)
                if txt_kilometraje.value.isdigit()
                else 0
            )

            unidad = Unidad(
                noeconomico=txt_economico.value,
                placas=txt_placas.value,
                modelo=txt_modelo.value,
                marca=txt_marca.value,
                año=anio_val,
                kilometraje=km_val,
                estatus="Activo",
            )

            if id_unidad_edicion is None:
                dao.insertar(unidad)
            else:
                unidad.id = id_unidad_edicion
                dao.actualizar(unidad)

            modal_agregar.open = False
            limpiar_formulario()
            cargar_unidades()
            page.update()

        except Exception as ex:
            lbl_error.value = f"Error al guardar: {str(ex)}"
            page.update()

    txt_titulo_modal = ft.Text(
        "Ingresar unidad",
        size=20,
        weight=ft.FontWeight.BOLD,
    )

    modal_agregar = ft.AlertDialog(
        content=ft.Container(
            width=400,
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    txt_titulo_modal,
                    txt_economico,
                    txt_placas,
                    txt_modelo,
                    txt_marca,
                    txt_anio,
                    txt_kilometraje,
                    lbl_error,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                "Cancelar",
                                bgcolor="#F97316",
                                color="white",
                                on_click=cerrar_modal_agregar,
                            ),
                            ft.ElevatedButton(
                                "Aceptar",
                                bgcolor="#6366F1",
                                color="white",
                                on_click=guardar_unidad,
                            ),
                        ],
                    ),
                ],
            ),
        )
    )

    def editar_unidad(unidad):
        global id_unidad_edicion

        id_unidad_edicion = unidad.id
        txt_titulo_modal.value = "Editar unidad"

        txt_economico.value = str(unidad.noeconomico or "")
        txt_placas.value = str(unidad.placas or "")
        txt_modelo.value = str(unidad.modelo or "")
        txt_marca.value = str(unidad.marca or "")
        txt_anio.value = str(unidad.año or "")
        txt_kilometraje.value = str(unidad.kilometraje or "")

        if modal_agregar not in page.overlay:
            page.overlay.append(modal_agregar)

        modal_agregar.open = True
        page.update()

    def abrir_modal_agregar(e):
        limpiar_formulario()
        txt_titulo_modal.value = "Ingresar unidad"

        if modal_agregar not in page.overlay:
            page.overlay.append(modal_agregar)

        modal_agregar.open = True
        page.update()

    def abrir_modal_agregar(e):
        limpiar_formulario()
        txt_titulo_modal.value = "Ingresar unidad"

        if modal_agregar not in page.overlay:
            page.overlay.append(modal_agregar)

        modal_agregar.open = True
        page.update()

    # --- 4. BUSCADOR Y BOTÓN INGRESAR ---
    buscador = ft.TextField(
        hint_text="Buscar unidad",
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
                    "Ingresar unidad",
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
        controls=[
            ft.Container(width=380, content=buscador),
            btn_ingresar,
        ],
    )

    cargar_unidades()

    # --- 5. LÓGICA DE NAVEGACIÓN Y SCROLL ---
    def deslizar_derecha(e):
        carrusel_listview.scroll_to(
            offset=1000,
            duration=350,
        )
        page.update()

    def deslizar_izquierda(e):
        carrusel_listview.scroll_to(
            offset=0,
            duration=350,
        )
        page.update()
        
    btn_prev = ft.Container(
        width=36,
        height=36,
        bgcolor="#F59E0B",
        border_radius=18,
        alignment=ft.Alignment(0, 0),
        on_click=deslizar_izquierda,
        content=ft.Icon(ft.Icons.CHEVRON_LEFT_ROUNDED, color="white", size=24),
    )

    btn_next = ft.Container(
        width=36,
        height=36,
        bgcolor="#F59E0B",
        border_radius=18,
        alignment=ft.Alignment(0, 0),
        on_click=deslizar_derecha,
        content=ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color="white", size=24),
    )

    seccion_carrusel = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            btn_prev,
            ft.Container(
                width=730,
                height=320,
                content=carrusel_listview,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            btn_next,
        ],
    )

    # --- ÁREA DE TRABAJO PRINCIPAL ---
    area_trabajo = ft.Container(
        expand=True,
        bgcolor="#FAFAFA",
        padding=ft.Padding(25, 15, 25, 20),
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Unidades",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                barra_controles,
                ft.Container(height=5),
                seccion_carrusel,
            ],
        ),
    )

    # --- ESTRUCTURA PRINCIPAL ---
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