import flet as ft
import traceback

try:
    from dao.pagos_dao import PagoDAO
    from dao.chofer_dao import ChoferDAO
    from models.pago import Pago
except ImportError as ex:
    print(f"[vista_pagos] ERROR al importar PagoDAO/ChoferDAO/Pago: {ex}")
    PagoDAO = None
    ChoferDAO = None
    Pago = None


# ==========================================
# VISTA PAGOS (COMPLETA Y COMPATIBLE)
# ==========================================
def vista_pagos(page: ft.Page, ir_a):
    page.title = "UniRuta - Pagos"

    dao = PagoDAO() if PagoDAO else None
    chofer_dao = ChoferDAO() if ChoferDAO else None

    # Variable de estado para controlar si editamos o creamos
    id_pago_edicion = None

    # Usuario de sesión
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = getattr(usuario, "nombre", "Natalia Sosa Rodriguez") if usuario else "Natalia Sosa Rodriguez"
    rol_usuario = getattr(usuario, "rol", "Administrador") if usuario else "Administrador"

    # --- SNACKBAR DE ÉXITO / ERROR ---
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
        snack_exito.content.controls[1].value = mensaje
        snack_exito.bgcolor = "#10B981"
        snack_exito.content.controls[0].name = ft.Icons.CHECK_CIRCLE
        _mostrar_snack()

    def mostrar_error(mensaje):
        snack_exito.content.controls[1].value = mensaje
        snack_exito.bgcolor = "#EF4444"
        snack_exito.content.controls[0].name = ft.Icons.ERROR_OUTLINE
        _mostrar_snack()

    def _mostrar_snack():
        if hasattr(page, "open"):
            page.open(snack_exito)
        else:
            if snack_exito not in page.overlay:
                page.overlay.append(snack_exito)
            snack_exito.open = True
            page.update()

    # --- LÓGICA DE DIÁLOGOS DE CABECERA (HEADER) ---
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
                        leading=ft.Icon(ft.Icons.ATTACH_MONEY, color="#3B82F6"),
                        title=ft.Text("Pagos pendientes", size=13),
                        subtitle=ft.Text("Revisa los pagos pendientes del periodo.", size=11),
                    ),
                ],
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo))],
        )
        abrir_dialogo(dialogo)

    # AUXILIARES PARA MANEJAR DIÁLOGOS (compatible con distintas versiones de Flet)
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

    # --- BARRA SUPERIOR (HEADER) ---
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
                    ft.Text(nombre_usuario, size=12, weight=ft.FontWeight.BOLD, color="#1E293B"),
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
        height=58,
        bgcolor="white",
        padding=ft.Padding(10, 0, 20, 0),
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
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
                    ft.Text(texto, color=color_txt, size=13, weight=(ft.FontWeight.BOLD if activo else ft.FontWeight.W_500)),
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
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes"),
                item_sidebar("Unidades", ft.Icons.DIRECTIONS_BUS_OUTLINED, "unidades"),
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos", activo=True),
            ],
        ),
    )

    # --- COMPONENTES DEL FORMULARIO Y MODAL ---
    txt_titulo_modal = ft.Text("Ingresar pago", size=22, weight=ft.FontWeight.BOLD, color="#0F172A")

    def _opciones_choferes():
        opciones = []
        if not chofer_dao:
            return opciones
        try:
            for c in chofer_dao.obtener_todos():
                cid = getattr(c, "id", None)
                cnombre = getattr(c, "nombre", f"Chofer {cid}")
                if cid is not None:
                    opciones.append(ft.dropdown.Option(key=str(cid), text=cnombre))
        except Exception:
            opciones = []
        return opciones

    txt_id_viaje_inner = ft.TextField(
        hint_text="EJ. 1024",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    txt_id_viaje = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_id_viaje_inner,
    )

    dd_chofer_inner = ft.Dropdown(
        hint_text="Seleccionar chofer",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        options=_opciones_choferes(),
        expand=True,
    )
    dd_chofer = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_chofer_inner,
    )

    txt_pago_base_inner = ft.TextField(
        hint_text="EJ. 1500.00",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    txt_pago_base = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_pago_base_inner,
    )

    txt_pago_inicial_inner = ft.TextField(
        hint_text="EJ. 500.00",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    txt_pago_inicial = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_pago_inicial_inner,
    )

    txt_pago_final_inner = ft.TextField(
        hint_text="EJ. 1000.00",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    txt_pago_final = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_pago_final_inner,
    )

    txt_total_acumulado_inner = ft.TextField(
        hint_text="EJ. 1500.00",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    txt_total_acumulado = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_total_acumulado_inner,
    )

    dd_metodo_pago_inner = ft.Dropdown(
        hint_text="Seleccionar método",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        options=[
            ft.dropdown.Option("Pago en Tarjeta"),
            ft.dropdown.Option("Pago en Efectivo"),
            ft.dropdown.Option("Transferencia"),
        ],
        expand=True,
    )
    dd_metodo_pago = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_metodo_pago_inner,
    )

    dd_periodo_pago_inner = ft.Dropdown(
        hint_text="Seleccionar periodo",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        options=[
            ft.dropdown.Option("Semanal"),
            ft.dropdown.Option("Quincenal"),
            ft.dropdown.Option("Mensual"),
        ],
        expand=True,
    )
    dd_periodo_pago = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_periodo_pago_inner,
    )

    def restablecer_formulario():
        nonlocal id_pago_edicion
        id_pago_edicion = None
        txt_titulo_modal.value = "Ingresar pago"
        txt_id_viaje_inner.value = ""
        dd_chofer_inner.options = _opciones_choferes()
        dd_chofer_inner.value = None
        txt_pago_base_inner.value = ""
        txt_pago_inicial_inner.value = ""
        txt_pago_final_inner.value = ""
        txt_total_acumulado_inner.value = ""
        dd_metodo_pago_inner.value = None
        dd_periodo_pago_inner.value = None

    def guardar_pago(e):
        nonlocal id_pago_edicion

        # --- Validación de campos obligatorios ---
        if not txt_id_viaje_inner.value or not str(txt_id_viaje_inner.value).strip():
            mostrar_error("El ID de viaje es obligatorio")
            return
        if not dd_chofer_inner.value:
            mostrar_error("Selecciona el chofer asignado")
            return
        if not dd_metodo_pago_inner.value:
            mostrar_error("Selecciona el método de pago")
            return
        if not dd_periodo_pago_inner.value:
            mostrar_error("Selecciona el periodo de pago")
            return

        try:
            id_viaje = int(txt_id_viaje_inner.value)
            id_chofer = int(dd_chofer_inner.value)
            pago_base = float(txt_pago_base_inner.value or 0)
            pago_inicial = float(txt_pago_inicial_inner.value or 0)
            pago_final = float(txt_pago_final_inner.value or 0)
            total_acumulado = float(txt_total_acumulado_inner.value or 0)
        except ValueError:
            mostrar_error("ID de viaje y montos deben ser numéricos")
            return

        if not Pago or not dao:
            mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
            return

        exito = False
        mensaje = ""

        try:
            if id_pago_edicion is None:
                nuevo_id = dao.obtener_ultimo_id() + 1
                pago_obj = Pago(
                    id=nuevo_id,
                    id_viaje=id_viaje,
                    id_chofer=id_chofer,
                    pago_base=pago_base,
                    pago_inicial=pago_inicial,
                    pago_final=pago_final,
                    total_acumulado=total_acumulado,
                    metodo_pago=dd_metodo_pago_inner.value,
                    periodo_pago=dd_periodo_pago_inner.value,
                )
                dao.insertar(pago_obj)
                exito = True
                mensaje = "Pago ingresado con éxito"
            else:
                pago_obj = Pago(
                    id=id_pago_edicion,
                    id_viaje=id_viaje,
                    id_chofer=id_chofer,
                    pago_base=pago_base,
                    pago_inicial=pago_inicial,
                    pago_final=pago_final,
                    total_acumulado=total_acumulado,
                    metodo_pago=dd_metodo_pago_inner.value,
                    periodo_pago=dd_periodo_pago_inner.value,
                )
                dao.actualizar(pago_obj)
                exito = True
                mensaje = "Pago actualizado con éxito"
        except Exception as ex:
            print(f"[vista_pagos] Error al guardar/actualizar: {ex}")
            mostrar_error("Ocurrió un error al guardar el pago (revisa la consola/terminal)")
            return

        restablecer_formulario()
        cerrar_dialogo(modal_agregar)
        cargar_datos_tabla()

        if exito:
            mostrar_exito(mensaje)

    def cancelar_modal(e):
        restablecer_formulario()
        cerrar_dialogo(modal_agregar)

    modal_content = ft.Container(
        width=520,
        padding=ft.Padding(20, 15, 20, 20),
        bgcolor="white",
        border_radius=12,
        content=ft.Column(
            tight=True,
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                txt_titulo_modal,
                ft.Row(
                    spacing=20,
                    controls=[
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("ID Viaje", size=11, color="#475569"),
                                txt_id_viaje,
                                ft.Text("Chofer asignado", size=11, color="#475569"),
                                dd_chofer,
                                ft.Text("Pago base", size=11, color="#475569"),
                                txt_pago_base,
                                ft.Text("Pago inicial", size=11, color="#475569"),
                                txt_pago_inicial,
                            ],
                        ),
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Pago final", size=11, color="#475569"),
                                txt_pago_final,
                                ft.Text("Total acumulado", size=11, color="#475569"),
                                txt_total_acumulado,
                                ft.Text("Método de pago", size=11, color="#475569"),
                                dd_metodo_pago,
                                ft.Text("Periodo de pago", size=11, color="#475569"),
                                dd_periodo_pago,
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Aceptar", bgcolor="#6366F1", color="white", expand=True, on_click=guardar_pago),
                        ft.ElevatedButton("Cancelar", bgcolor="#F97316", color="white", expand=True, on_click=cancelar_modal),
                    ],
                ),
            ],
        ),
    )

    modal_agregar = ft.AlertDialog(
        content=modal_content,
        bgcolor="white",
        shape=ft.RoundedRectangleBorder(radius=12),
    )

    def abrir_modal_agregar(e):
        restablecer_formulario()
        abrir_dialogo(modal_agregar)

    def abrir_modal_editar(pago_item):
        nonlocal id_pago_edicion
        id_pago_edicion = obtener_valor(pago_item, "id", None)

        txt_titulo_modal.value = "Editar pago"
        txt_id_viaje_inner.value = str(obtener_valor(pago_item, "id_viaje", ""))
        dd_chofer_inner.options = _opciones_choferes()
        dd_chofer_inner.value = str(obtener_valor(pago_item, "id_chofer", "")) or None
        txt_pago_base_inner.value = str(obtener_valor(pago_item, "pago_base", 0))
        txt_pago_inicial_inner.value = str(obtener_valor(pago_item, "pago_inicial", 0))
        txt_pago_final_inner.value = str(obtener_valor(pago_item, "pago_final", 0))
        txt_total_acumulado_inner.value = str(obtener_valor(pago_item, "total_acumulado", 0))
        dd_metodo_pago_inner.value = str(obtener_valor(pago_item, "metodo_pago", "")) or None
        dd_periodo_pago_inner.value = str(obtener_valor(pago_item, "periodo_pago", "")) or None

        abrir_dialogo(modal_agregar)

    # --- MODAL DE CONFIRMACIÓN DE ELIMINACIÓN ---
    def confirmar_eliminar(id_pago, chofer_nombre=""):
        if id_pago is None:
            mostrar_error("No se pudo identificar el pago a eliminar")
            return

        def borrar_y_cerrar(e):
            print(f"[vista_pagos] Click en Aceptar-eliminar. id_pago={id_pago!r}, dao={'OK' if dao else 'None'}")
            try:
                if not dao:
                    mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
                    cerrar_dialogo(dialogo_eliminar)
                    return

                dao.eliminar(id_pago)
                print(f"[vista_pagos] dao.eliminar({id_pago!r}) ejecutado sin excepción")
                cargar_datos_tabla()
                cerrar_dialogo(dialogo_eliminar)
                mostrar_exito("Pago eliminado con éxito")
            except ValueError as ve:
                print(f"[vista_pagos] No se pudo eliminar: {ve}")
                cerrar_dialogo(dialogo_eliminar)
                mostrar_error(str(ve))
            except Exception:
                print("[vista_pagos] EXCEPCIÓN al eliminar:")
                traceback.print_exc()
                try:
                    cerrar_dialogo(dialogo_eliminar)
                except Exception:
                    pass
                mostrar_error("Ocurrió un error al eliminar el pago (revisa la consola/terminal)")

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
                            f"¿Estas seguro de eliminar el pago de {chofer_nombre or 'este registro'}?",
                            size=16,
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

    # --- TABLA Y BUSCADOR ---
    txt_buscar = ft.TextField(
        hint_text="EJ. Carlos Mendoza",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: cargar_datos_tabla(e.control.value),
    )

    container_buscar = ft.Container(
        width=450,
        height=38,
        bgcolor="white",
        border=ft.Border.all(1, "#E2E8F0"),
        border_radius=20,
        content=txt_buscar,
    )

    tabla_pagos = ft.DataTable(
        bgcolor="white",
        heading_row_color="#FC9210",
        heading_row_height=42,
        data_row_min_height=52,
        column_spacing=18,
        columns=[
            ft.DataColumn(ft.Text("ID", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("ID Viaje", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Chofer asignado", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Pago base", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Pago inicial", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Pago final", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Total acumulado", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Método pago", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Periodo de pago", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color="white", size=11, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def obtener_valor(item, clave, valor_defecto="-"):
        if isinstance(item, dict):
            return item.get(clave) or valor_defecto
        return getattr(item, clave, valor_defecto) or valor_defecto

    def color_por_metodo(metodo_str):
        m = metodo_str.strip().lower()
        if "efectivo" in m:
            return "#10B981"       # verde
        if "transferencia" in m:
            return "#6366F1"       # violeta
        return "#2563EB"           # azul (tarjeta u otro)

    def cargar_datos_tabla(filtro=""):
        lista = []
        if dao:
            try:
                lista = dao.obtener_todos()
            except Exception:
                print("[vista_pagos] EXCEPCIÓN al obtener pagos:")
                traceback.print_exc()
                lista = []

        # PagoDAO no expone un método de búsqueda propio, así que
        # filtramos por nombre de chofer del lado del cliente.
        if filtro.strip():
            f = filtro.strip().lower()
            lista = [p for p in lista if f in str(obtener_valor(p, "nombre_chofer", "")).lower()]

        filas = []
        for p in lista:
            id_p = obtener_valor(p, "id", None)
            id_viaje_p = obtener_valor(p, "id_viaje", "-")
            nombre_chofer_p = obtener_valor(p, "nombre_chofer", "-")
            pago_base_p = obtener_valor(p, "pago_base", 0)
            pago_inicial_p = obtener_valor(p, "pago_inicial", 0)
            pago_final_p = obtener_valor(p, "pago_final", 0)
            total_acumulado_p = obtener_valor(p, "total_acumulado", 0)
            metodo_str = str(obtener_valor(p, "metodo_pago", "Pago en Tarjeta"))
            periodo_str = str(obtener_valor(p, "periodo_pago", "Quincenal"))

            color_met = color_por_metodo(metodo_str)
            icono_metodo = ft.Icons.MONEY if "efectivo" in metodo_str.lower() else ft.Icons.CREDIT_CARD

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_p), size=11, color="#1E293B")),
                        ft.DataCell(ft.Text(str(id_viaje_p), size=11, color="#475569")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Icon(ft.Icons.PERSON, size=14, color="white"),
                                        bgcolor="#93C5FD",
                                        radius=14,
                                    ),
                                    ft.Text(str(nombre_chofer_p), size=11, color="#1E293B", weight=ft.FontWeight.W_500),
                                ],
                                spacing=8,
                            )
                        ),
                        ft.DataCell(ft.Text(f"${float(pago_base_p or 0):.2f}", size=11, color="#1E293B", weight=ft.FontWeight.BOLD)),
                        ft.DataCell(
                            ft.Container(
                                bgcolor="#F1F5F9",
                                border_radius=6,
                                padding=ft.Padding(6, 2, 6, 2),
                                content=ft.Text(f"${float(pago_inicial_p or 0):.2f}", size=11, color="#1E293B", weight=ft.FontWeight.BOLD),
                            )
                        ),
                        ft.DataCell(ft.Text(f"${float(pago_final_p or 0):.2f}", size=11, color="#1E293B", weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"${float(total_acumulado_p or 0):.2f}", size=11, color="#1E293B", weight=ft.FontWeight.BOLD)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Icon(icono_metodo, size=15, color=color_met),
                                    ft.Text(metodo_str, size=11, color=color_met, weight=ft.FontWeight.W_500),
                                ],
                                spacing=4,
                            )
                        ),
                        ft.DataCell(ft.Text(periodo_str, size=11, color="#475569")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Container(
                                        width=26,
                                        height=26,
                                        border=ft.Border.all(1.5, "#F97316"),
                                        border_radius=13,
                                        alignment=ft.Alignment(0, 0),
                                        tooltip="Editar",
                                        on_click=lambda e, pago_item=p: abrir_modal_editar(pago_item),
                                        content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=14, color="#F97316"),
                                    ),
                                    ft.Container(
                                        width=26,
                                        height=26,
                                        border=ft.Border.all(1.5, "#EF4444"),
                                        border_radius=13,
                                        alignment=ft.Alignment(0, 0),
                                        tooltip="Eliminar",
                                        on_click=lambda e, i=id_p, n=nombre_chofer_p: confirmar_eliminar(i, n),
                                        content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=14, color="#EF4444"),
                                    ),
                                ],
                                spacing=8,
                            )
                        ),
                    ]
                )
            )
        tabla_pagos.rows = filas
        try:
            page.update()
        except Exception:
            pass

    btn_agregar_pago = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="white", size=16), ft.Text("Agregar pago", color="white", size=12)],
            tight=True,
            spacing=4,
        ),
        bgcolor="#FC9210",
        on_click=abrir_modal_agregar,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
    )

    cargar_datos_tabla()

    contenido_tabla_pagos = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Pagos", size=26, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Container(height=10),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[container_buscar, btn_agregar_pago],
                spacing=15,
            ),
            ft.Container(height=20),
            ft.Container(
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color="#1A000000", offset=ft.Offset(0, 4)),
                content=tabla_pagos,
            ),
        ],
    )

    # --- PANTALLA DE VERIFICACIÓN (SOLO ADMINISTRADORES) ---
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
                ft.Text("Ingrese sus datos", size=26, weight=ft.FontWeight.BOLD, color="#000000"),
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
                    content=ft.Text("Aceptar", color="white", size=13, weight=ft.FontWeight.BOLD),
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
                    ft.Text("Pagos", size=24, weight=ft.FontWeight.BOLD, color="#1E293B"),
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, -0.15),
                        content=card_autenticacion,
                    ),
                ],
            ),
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