import flet as ft
from dao.viaje_dao import ViajeDAO
from models.viaje import Viaje
from dao.unidad_dao import UnidadDAO
from dao.chofer_dao import ChoferDAO
from dao.ruta_dao import RutaDAO
import traceback
import unicodedata


def normalizar_texto(texto):
    """Quita espacios, mayúsculas y acentos para comparar de forma segura
    (mismo helper que usa vista_choferes)."""
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    return texto


def vista_viajes(page: ft.Page, ir_a):
    page.title = "UniRuta - Viajes"

    # Instancia del DAO
    dao = ViajeDAO() if "ViajeDAO" in globals() else None
    unidad_dao = UnidadDAO()
    chofer_dao = ChoferDAO()
    ruta_dao = RutaDAO()

    # Variable para saber si estamos editando
    id_viaje_edicion = None

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

    # --- SNACKBAR DE ÉXITO / ERROR (mismo estilo que choferes) ---
    snack_exito = ft.SnackBar(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="white", size=20),
                ft.Text("", color="white", size=13, weight=ft.FontWeight.BOLD),
            ],
            spacing=10,
        ),
        bgcolor="#10B981",
        duration=2500,
    )

    if snack_exito not in page.overlay:
        page.overlay.append(snack_exito)

    def mostrar_exito(mensaje):
        try:
            snack_exito.content.controls[1].value = mensaje
            snack_exito.bgcolor = "#10B981"
            snack_exito.content.controls[0].name = ft.Icons.CHECK_CIRCLE
            _mostrar_snack()
        except Exception as ex:
            print(f"[vista_viajes] Error al mostrar snackbar de éxito: {ex}")
            traceback.print_exc()

    def mostrar_error(mensaje):
        try:
            snack_exito.content.controls[1].value = mensaje
            snack_exito.bgcolor = "#EF4444"
            snack_exito.content.controls[0].name = ft.Icons.ERROR_OUTLINE
            _mostrar_snack()
        except Exception as ex:
            print(f"[vista_viajes] Error al mostrar snackbar de error: {ex}")
            traceback.print_exc()

    def _mostrar_snack():
        # Reubica el snackbar al final del overlay para que quede por
        # encima del modal (que también vive en el overlay), evitando
        # que la alerta quede oculta detrás del AlertDialog abierto.
        if snack_exito in page.overlay:
            page.overlay.remove(snack_exito)
        page.overlay.append(snack_exito)

        if hasattr(page, "open"):
            page.open(snack_exito)
        else:
            snack_exito.open = True
            page.update()

    def mostrar_alerta_modal(mensaje, es_error=True):
        """Alerta tipo diálogo para usarse MIENTRAS el modal de
        Programar/Editar viaje está abierto. Un SnackBar nunca se
        dibuja por encima de un AlertDialog abierto en Flet, así que
        para esos casos usamos otro AlertDialog (que sí se apila por
        encima) en vez del snackbar."""
        color_icono = "#EF4444" if es_error else "#10B981"
        icono = ft.Icons.ERROR_OUTLINE if es_error else ft.Icons.CHECK_CIRCLE

        dialogo_alerta = ft.AlertDialog(
            bgcolor="white",
            shape=ft.RoundedRectangleBorder(radius=12),
            content=ft.Container(
                width=380,
                padding=ft.Padding(15, 20, 15, 10),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    controls=[
                        ft.Icon(icono, color=color_icono, size=40),
                        ft.Text(
                            mensaje,
                            size=14,
                            color="#0F172A",
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Entendido",
                            bgcolor="#6366F1",
                            color="white",
                            width=180,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                            on_click=lambda e: cerrar_dialogo(dialogo_alerta),
                        ),
                    ],
                ),
            ),
        )
        abrir_dialogo(dialogo_alerta)

    # --- LÓGICA DE DIÁLOGOS DE CABECERA (HEADER) ---
    def cerrar_sesion(e):
        if hasattr(page, "usuario_actual"):
            page.usuario_actual = None
        ir_a("login")

    def abrir_dialogo(dlg):
        if hasattr(page, "open"):
            page.open(dlg)
        else:
            if dlg not in page.overlay:
                page.overlay.append(dlg)
            page.dialog = dlg
            dlg.open = True
            page.update()

    def cerrar_dialogo(dlg):
        if hasattr(page, "close"):
            page.close(dlg)
        else:
            dlg.open = False
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
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo))],
        )
        abrir_dialogo(dialogo)

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

    # --- 3. TABLA (con columna de Observaciones agregada) ---
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
                    "Hora de llegada",
                    color="white",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.DataColumn(
                ft.Text(
                    "Pasajeros",
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
                    "Obs.",
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

    dd_unidad = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_unidad_inner,
    )

    def cargar_dropdowns():
        # UNIDADES
        dd_unidad_inner.options = [
            ft.dropdown.Option(key=str(u.id), text=u.noeconomico)
            for u in unidad_dao.obtener_todos()
        ]

        # CHOFERES
        dd_chofer_inner.options = [
            ft.dropdown.Option(key=str(c.id), text=c.nombre)
            for c in chofer_dao.obtener_todos()
        ]

        # RUTAS
        dd_ruta_inner.options = [
            ft.dropdown.Option(key=str(r.id), text=r.nombre)
            for r in ruta_dao.obtener_todos()
        ]

    def restablecer_formulario():
        nonlocal id_viaje_edicion
        id_viaje_edicion = None
        txt_titulo_modal.value = "Programar viaje"
        txt_fecha_inner.value = ""
        txt_hora_inner.value = ""
        txt_hora_llegada_inner.value = ""
        txt_pasajeros_inner.value = ""
        txt_observaciones_inner.value = ""
        dd_unidad_inner.value = None
        dd_chofer_inner.value = None
        dd_ruta_inner.value = None
        dd_estatus_inner.value = "Programado"

    ESTATUS_OPCIONES_VIAJE = ["Programado", "En curso", "Concluido", "Cancelado"]

    def normalizar_estatus_viaje(valor):
        """Empareja el estatus guardado en BD con el valor exacto del
        Dropdown (mismas mayúsculas/acentos), para que no quede
        desincronizado y bloquee el guardado silenciosamente."""
        if not valor:
            return "Programado"
        valor_str = str(valor).strip()
        for opcion in ESTATUS_OPCIONES_VIAJE:
            if opcion.lower() == valor_str.lower():
                return opcion
        return "Programado"

    def guardar_viaje(e):
        nonlocal id_viaje_edicion

        print("[vista_viajes] guardar_viaje: click en Guardar")

        campos_obligatorios = [
            txt_fecha_inner.value,
            txt_hora_inner.value,
            dd_unidad_inner.value,
            dd_chofer_inner.value,
            dd_ruta_inner.value,
            dd_estatus_inner.value,
        ]
        if not all(c and str(c).strip() for c in campos_obligatorios):
            mostrar_alerta_modal("No hay ningún campo registrado")
            return

        if not dao:
            mostrar_alerta_modal("No hay conexión con la base de datos (revisa la consola/terminal)")
            return

        rutas = ruta_dao.obtener_todos()
        origen = ""
        destino = ""
        for ruta in rutas:
            if str(ruta.id) == str(dd_ruta_inner.value):
                origen = ruta.origen
                destino = ruta.destino
                break

        observaciones_valor = (
            str(txt_observaciones_inner.value).strip()
            if txt_observaciones_inner.value and str(txt_observaciones_inner.value).strip()
            else None
        )

        hora_llegada_valor = (
            str(txt_hora_llegada_inner.value).strip()
            if txt_hora_llegada_inner.value and str(txt_hora_llegada_inner.value).strip()
            else None
        )

        pasajeros_valor = (
            str(txt_pasajeros_inner.value).strip()
            if txt_pasajeros_inner.value and str(txt_pasajeros_inner.value).strip()
            else None
        )

        viaje = Viaje(
            id=id_viaje_edicion,
            fecha=txt_fecha_inner.value,
            hora=txt_hora_inner.value,
            hora_llegada=hora_llegada_valor,
            pasajeros=pasajeros_valor,
            observaciones=observaciones_valor,
            id_unidad=dd_unidad_inner.value,
            id_chofer=dd_chofer_inner.value,
            id_ruta=dd_ruta_inner.value,
            estatus=dd_estatus_inner.value,
        )

        viaje.origen = origen
        viaje.destino = destino

        mensaje = ""

        try:
            if id_viaje_edicion is None:
                dao.insertar(viaje)
                mensaje = "Viaje programado con éxito"
            else:
                if hasattr(dao, "actualizar"):
                    dao.actualizar(viaje)
                else:
                    dao.insertar(viaje)
                mensaje = "Viaje actualizado con éxito"
            print(f"[vista_viajes] guardar_viaje: guardado en BD OK -> {mensaje}")
        except Exception:
            print("[vista_viajes] ERROR al guardar/actualizar en BD:")
            traceback.print_exc()
            mostrar_alerta_modal("Ocurrió un error al guardar el viaje (revisa la consola/terminal)")
            return

        try:
            restablecer_formulario()
            cerrar_dialogo(modal_programar)
            cargar_datos_tabla()
            print("[vista_viajes] guardar_viaje: UI refrescada OK")
        except Exception:
            print("[vista_viajes] ERROR al refrescar la UI tras guardar:")
            traceback.print_exc()

        mostrar_exito(mensaje)

    def cancelar_modal(e):
        restablecer_formulario()
        cerrar_dialogo(modal_programar)

    def abrir_modal_programar(e):
        restablecer_formulario()
        cargar_dropdowns()
        abrir_dialogo(modal_programar)

    def editar_viaje(viaje):
        nonlocal id_viaje_edicion

        cargar_dropdowns()

        id_viaje_edicion = viaje.id

        txt_titulo_modal.value = "Editar viaje"

        txt_fecha_inner.value = str(getattr(viaje, "fecha", ""))
        txt_hora_inner.value = str(getattr(viaje, "hora", ""))

        hora_llegada_val = getattr(viaje, "hora_llegada", None)
        txt_hora_llegada_inner.value = (
            str(hora_llegada_val) if hora_llegada_val not in (None, "", "None") else ""
        )

        pasajeros_val = getattr(viaje, "pasajeros", None)
        txt_pasajeros_inner.value = (
            str(pasajeros_val) if pasajeros_val not in (None, "", "None") else ""
        )

        observaciones_val = getattr(viaje, "observaciones", "")
        txt_observaciones_inner.value = str(observaciones_val) if observaciones_val else ""

        id_unidad_val = getattr(viaje, "id_unidad", None)
        id_chofer_val = getattr(viaje, "id_chofer", None)
        id_ruta_val = getattr(viaje, "id_ruta", None)

        dd_unidad_inner.value = str(id_unidad_val) if id_unidad_val not in (None, "") else None
        dd_chofer_inner.value = str(id_chofer_val) if id_chofer_val not in (None, "") else None
        dd_ruta_inner.value = str(id_ruta_val) if id_ruta_val not in (None, "") else None
        dd_estatus_inner.value = normalizar_estatus_viaje(getattr(viaje, "estatus", "Programado"))

        abrir_dialogo(modal_programar)

    def mostrar_observacion(id_viaje_str, observacion):
        dialogo_observacion = ft.AlertDialog(
            bgcolor="white",
            shape=ft.RoundedRectangleBorder(radius=12),
            content=ft.Container(
                width=420,
                padding=ft.Padding(15, 20, 15, 10),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    controls=[
                        ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED, color="#6366F1", size=36),
                        ft.Text(
                            f"Observación del viaje {id_viaje_str}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            width=390,
                            bgcolor="#F8FAFC",
                            border=ft.Border.all(1, "#E2E8F0"),
                            border_radius=8,
                            padding=ft.Padding(12, 10, 12, 10),
                            content=ft.Text(
                                observacion or "-",
                                size=13,
                                color="#334155",
                                text_align=ft.TextAlign.LEFT,
                            ),
                        ),
                        ft.ElevatedButton(
                            "Cerrar",
                            bgcolor="#6366F1",
                            color="white",
                            width=200,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                            on_click=lambda e: cerrar_dialogo(dialogo_observacion),
                        ),
                    ],
                ),
            ),
        )
        abrir_dialogo(dialogo_observacion)

    # --- MODAL DE CONFIRMACIÓN DE ELIMINACIÓN (mismo estilo que choferes) ---
    def confirmar_eliminar(id_viaje):
        if id_viaje is None:
            mostrar_error("No se pudo identificar el viaje a eliminar")
            return

        def borrar_y_cerrar(e):
            try:
                if not dao or not hasattr(dao, "eliminar"):
                    mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
                    cerrar_dialogo(dialogo_eliminar)
                    return

                dao.eliminar(id_viaje)
            except ValueError as ve:
                print(f"[vista_viajes] No se pudo eliminar: {ve}")
                cerrar_dialogo(dialogo_eliminar)
                mostrar_error(str(ve))
                return
            except Exception:
                print("[vista_viajes] EXCEPCIÓN al eliminar en BD:")
                traceback.print_exc()
                try:
                    cerrar_dialogo(dialogo_eliminar)
                except Exception:
                    pass
                mostrar_error("Ocurrió un error al eliminar el viaje (revisa la consola/terminal)")
                return

            try:
                cerrar_dialogo(dialogo_eliminar)
                cargar_datos_tabla()
            except Exception:
                print("[vista_viajes] ERROR al refrescar la UI tras eliminar:")
                traceback.print_exc()

            mostrar_exito("Viaje eliminado con éxito")

        dialogo_eliminar = ft.AlertDialog(
            bgcolor="white",
            shape=ft.RoundedRectangleBorder(radius=12),
            content=ft.Container(
                width=420,
                padding=ft.Padding(15, 20, 15, 10),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Text(
                            "¿Estás seguro de eliminar este registro de viaje?",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Aceptar",
                                    bgcolor="#6366F1",
                                    color="white",
                                    expand=True,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                    on_click=borrar_y_cerrar,
                                ),
                                ft.ElevatedButton(
                                    "Cancelar",
                                    bgcolor="#F97316",
                                    color="white",
                                    expand=True,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                    on_click=lambda e: cerrar_dialogo(dialogo_eliminar),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )

        abrir_dialogo(dialogo_eliminar)

    def cargar_datos_tabla(filtro=""):
        lista = []
        if dao:
            try:
                if filtro.strip() and hasattr(dao, "buscar"):
                    # Si en algún momento el DAO agrega un método buscar()
                    # propio, se sigue respetando (búsqueda en BD).
                    lista = dao.buscar(filtro)
                elif hasattr(dao, "obtener_todos"):
                    lista = dao.obtener_todos()
            except Exception:
                print("[vista_viajes] Error al cargar datos de la tabla:")
                traceback.print_exc()
                lista = []

        lista = lista or []

        # ViajeDAO no expone buscar(), así que filtramos aquí mismo por
        # chofer, ruta, unidad, fecha, hora y estatus. Se busca por
        # palabra (todas deben coincidir, sin importar el orden), para
        # que "juan programado" encuentre el viaje aunque esos datos
        # no estén juntos ni en ese orden.
        filtro_norm = normalizar_texto(filtro)
        palabras_filtro = [p for p in filtro_norm.split() if p]
        if palabras_filtro:
            def coincide(v):
                campos = [
                    getattr(v, "id", ""),
                    getattr(v, "chofer_nombre", ""),
                    getattr(v, "ruta_nombre", ""),
                    getattr(v, "origen", ""),
                    getattr(v, "destino", ""),
                    getattr(v, "id_unidad", ""),
                    getattr(v, "fecha", ""),
                    getattr(v, "hora", ""),
                    getattr(v, "hora_llegada", ""),
                    getattr(v, "estatus", ""),
                ]
                texto = normalizar_texto(
                    " ".join(str(c) for c in campos if c not in (None, "", "None"))
                )
                return all(palabra in texto for palabra in palabras_filtro)

            lista = [v for v in lista if coincide(v)]

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

            # 6b. Hora de llegada
            hora_llegada_v = getattr(v, "hora_llegada", None)
            hora_llegada_display = str(hora_llegada_v) if hora_llegada_v not in (None, "", "None") else "-"

            # 6c. Pasajeros
            pasajeros_v = getattr(v, "pasajeros", None)
            pasajeros_display = str(pasajeros_v) if pasajeros_v not in (None, "", "None") else "-"

            # 7. Estatus y Colores
            estatus = str(getattr(v, "estatus", "Inactivo")).capitalize()
            estatus_lower = estatus.lower()

            if "curso" in estatus_lower or "programado" in estatus_lower:
                color_estatus = "#10B981"  # Verde
            elif "concluido" in estatus_lower or "finalizado" in estatus_lower:
                color_estatus = "#EC932F"  # Naranja
            else:
                color_estatus = "#64748B"  # Gris

            # 8. Observaciones (mismo comportamiento que en choferes)
            observaciones_v = getattr(v, "observaciones", None)
            tiene_observaciones = bool(
                observaciones_v and str(observaciones_v).strip() not in ["", "-", "None"]
            )
            if tiene_observaciones:
                celda_observaciones = ft.Container(
                    tooltip=str(observaciones_v).strip(),
                    on_click=lambda e, i=id_viaje, obs=str(observaciones_v).strip(): mostrar_observacion(i, obs),
                    content=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED, size=16, color="#6366F1"),
                )
            else:
                celda_observaciones = ft.Text("-", size=11, color="#CBD5E1")

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
                            ft.Container(
                                padding=ft.Padding(12, 3, 12, 3),
                                border=ft.Border.all(1, "#CBD5E1"),
                                border_radius=12,
                                content=ft.Text(
                                    hora_llegada_display, size=11, color="#1E293B"
                                ),
                            )
                        ),
                        ft.DataCell(
                            ft.Text(pasajeros_display, size=11, color="#1E293B")
                        ),
                        ft.DataCell(
                            ft.Text(
                                estatus,
                                size=11,
                                color=color_estatus,
                                weight=ft.FontWeight.BOLD,
                            )
                        ),
                        ft.DataCell(celda_observaciones),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#EC932F"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        tooltip="Editar",
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
                                        tooltip="Eliminar",
                                        on_click=lambda e, uid=id_v: confirmar_eliminar(uid),
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
        try:
            page.update()
        except Exception:
            pass

    def al_cambiar_buscador(e):
        cargar_datos_tabla(e.control.value)

    # --- 4. CONTROLES Y BUSCADOR ---
    buscador = ft.TextField(
        hint_text="Busca por chofer, ruta, unidad, fecha o estatus",
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
        bgcolor="white",
        shape=ft.RoundedRectangleBorder(radius=12),
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
                                on_click=cancelar_modal,
                            ),
                        ]
                    ),
                ],
            ),
        )
    )

    # NOTA: se eliminó el registro manual de modal_programar en
    # page.overlay que existía aquí antes. abrir_dialogo() ya llama a
    # page.open(dlg), que en Flet 0.86 se encarga de agregarlo al
    # overlay por sí solo. Tenerlo registrado dos veces (aquí y dentro
    # de page.open) hacía que page.close(dlg) no cerrara correctamente
    # el modal en algunos casos (ej. botón "Cancelar").

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

    barra_controles = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[ft.Container(width=420, content=buscador), btn_programar],
    )

    cargar_datos_tabla()

    contenedor_tabla = ft.Container(
        bgcolor="white",
        border_radius=8,
        expand=True,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 3),
        ),
        content=ft.Row(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[tabla_viajes],
                ),
            ],
        ),
    )

    # --- ÁREA DE TRABAJO ---
    area_trabajo = ft.Container(
        expand=True,
        bgcolor="#FAFAFA",
        padding=ft.Padding(25, 15, 25, 20),
        content=ft.Column(
            expand=True,
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