import flet as ft
import traceback

try:
    from dao.ruta_dao import RutaDAO
    from models.ruta import Ruta
except ImportError as ex:
    print(f"[vista_rutas] ERROR al importar RutaDAO/Ruta: {ex}")
    RutaDAO = None
    Ruta = None


# ==========================================
# VISTA RUTAS (COMPLETA Y COMPATIBLE)
# ==========================================
def vista_rutas(page: ft.Page, ir_a):
    page.title = "UniRuta - Rutas"

    dao = RutaDAO() if RutaDAO else None

    # Estado: si estamos editando, guarda el id de la ruta en edición
    id_ruta_edicion = None

    # Usuario actual de la sesión (fallback a "Juana Suarez" si no hay datos)
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = getattr(usuario, "nombre", "Juana Suarez") if usuario else "Juana Suarez"
    rol_usuario = getattr(usuario, "rol", "Administrador") if usuario else "Administrador"
    correo_usuario = (
        getattr(usuario, "correo", getattr(usuario, "email", "usuario@uniruta.com"))
        if usuario
        else "usuario@uniruta.com"
    )

    # --- SNACKBAR DE ÉXITO ---
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

    # --- SNACKBAR DE ERROR (validaciones) ---
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
                        leading=ft.Icon(ft.Icons.BADGE_OUTLINED, color="#3B82F6"),
                        title=ft.Text("Licencia por vencer", size=13),
                        subtitle=ft.Text("Revisa la vigencia de los choferes.", size=11),
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
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas", activo=True),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- 3. CAMPOS DEL FORMULARIO / MODAL DE INGRESAR-EDITAR RUTA ---
    txt_titulo_modal = ft.Text("Ingresar ruta", size=22, weight=ft.FontWeight.BOLD, color="#0F172A")

    def campo(hint, multiline=False, min_lines=1, max_lines=1):
        inner = ft.TextField(
            hint_text=hint,
            border=ft.InputBorder.NONE,
            content_padding=ft.Padding(10, 8 if multiline else 0, 10, 8 if multiline else 0),
            text_size=12,
            multiline=multiline,
            min_lines=min_lines,
            max_lines=max_lines,
            expand=True,
        )
        contenedor = ft.Container(
            height=None if multiline else 40,
            bgcolor="#F8FAFC",
            border=ft.Border.all(1, "#CBD5E1"),
            border_radius=8,
            alignment=ft.Alignment(-1, -1 if multiline else 0),
            content=inner,
        )
        return inner, contenedor

    txt_nombre_inner, txt_nombre = campo("EJ. Huamantla - Apizaco")
    txt_origen_inner, txt_origen = campo("EJ. Huamantla")
    txt_destino_inner, txt_destino = campo("EJ. UTT")
    txt_tiempo_inner, txt_tiempo = campo("EJ. 00:15:00 (HH:MM:SS)")
    txt_tarifa_inner, txt_tarifa = campo("EJ. 25")
    txt_observaciones_inner, txt_observaciones = campo(
        "EJ. Ruta con desvío temporal por obras",
        multiline=True,
        min_lines=2,
        max_lines=3,
    )

    def restablecer_formulario():
        nonlocal id_ruta_edicion
        id_ruta_edicion = None
        txt_titulo_modal.value = "Ingresar ruta"
        txt_nombre_inner.value = ""
        txt_origen_inner.value = ""
        txt_destino_inner.value = ""
        txt_tiempo_inner.value = ""
        txt_tarifa_inner.value = ""
        txt_observaciones_inner.value = ""

    def guardar_ruta(e):
        nonlocal id_ruta_edicion

        # --- Validación de campos obligatorios ---
        campos_faltantes = []
        if not txt_nombre_inner.value or not str(txt_nombre_inner.value).strip():
            campos_faltantes.append("Nombre de la ruta")
        if not txt_origen_inner.value or not str(txt_origen_inner.value).strip():
            campos_faltantes.append("Origen")
        if not txt_destino_inner.value or not str(txt_destino_inner.value).strip():
            campos_faltantes.append("Destino")
        if not txt_tiempo_inner.value or not str(txt_tiempo_inner.value).strip():
            campos_faltantes.append("Tiempo estimado")

        if campos_faltantes:
            mostrar_aviso_formulario_incompleto(campos_faltantes)
            return

        tarifa_valor = None
        if txt_tarifa_inner.value and str(txt_tarifa_inner.value).strip():
            try:
                tarifa_valor = int(str(txt_tarifa_inner.value).strip())
            except ValueError:
                mostrar_error("La tarifa debe ser un número entero (ej. 25)")
                return

        if not Ruta or not dao:
            mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
            return

        observaciones_valor = (
            str(txt_observaciones_inner.value).strip()
            if txt_observaciones_inner.value and str(txt_observaciones_inner.value).strip()
            else None
        )

        exito = False
        mensaje = ""

        try:
            if id_ruta_edicion is None:
                nuevo_id = dao.obtener_ultimo_id() + 1
                ruta_obj = Ruta(
                    id=nuevo_id,
                    nombre=str(txt_nombre_inner.value).strip(),
                    origen=str(txt_origen_inner.value).strip(),
                    destino=str(txt_destino_inner.value).strip(),
                    tiempo_estimado=str(txt_tiempo_inner.value).strip(),
                    observaciones=observaciones_valor,
                    tarifa=tarifa_valor,
                )
                dao.insertar(ruta_obj)
                exito = True
                mensaje = "Ruta ingresada con éxito"
            else:
                ruta_obj = Ruta(
                    id=id_ruta_edicion,
                    nombre=str(txt_nombre_inner.value).strip(),
                    origen=str(txt_origen_inner.value).strip(),
                    destino=str(txt_destino_inner.value).strip(),
                    tiempo_estimado=str(txt_tiempo_inner.value).strip(),
                    observaciones=observaciones_valor,
                    tarifa=tarifa_valor,
                )
                dao.actualizar(ruta_obj)
                exito = True
                mensaje = "Ruta actualizada con éxito"
        except Exception as ex:
            print(f"[vista_rutas] Error al guardar/actualizar: {ex}")
            mostrar_error("Ocurrió un error al guardar la ruta (revisa la consola/terminal)")
            return

        restablecer_formulario()
        cerrar_dialogo(modal_ruta)
        cargar_datos_tabla()

        if exito:
            mostrar_exito(mensaje)

    def cancelar_modal(e):
        restablecer_formulario()
        cerrar_dialogo(modal_ruta)

    modal_content = ft.Container(
        width=520,
        padding=ft.Padding(20, 15, 20, 20),
        bgcolor="white",
        border_radius=12,
        content=ft.Column(
            tight=True,
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                txt_titulo_modal,
                ft.Text("Nombre de la ruta", size=11, color="#475569"),
                txt_nombre,
                ft.Row(
                    spacing=20,
                    controls=[
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Origen", size=11, color="#475569"),
                                txt_origen,
                            ],
                        ),
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Destino", size=11, color="#475569"),
                                txt_destino,
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=20,
                    controls=[
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Tiempo estimado", size=11, color="#475569"),
                                txt_tiempo,
                            ],
                        ),
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Tarifa (pesos)", size=11, color="#475569"),
                                txt_tarifa,
                            ],
                        ),
                    ],
                ),
                ft.Text("Observaciones", size=11, color="#475569"),
                txt_observaciones,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Aceptar", bgcolor="#6366F1", color="white", expand=True, on_click=guardar_ruta),
                        ft.ElevatedButton("Cancelar", bgcolor="#F97316", color="white", expand=True, on_click=cancelar_modal),
                    ],
                ),
            ],
        ),
    )

    modal_ruta = ft.AlertDialog(
        content=modal_content,
        bgcolor="white",
        shape=ft.RoundedRectangleBorder(radius=12),
    )

    def abrir_modal_agregar(e):
        restablecer_formulario()
        abrir_dialogo(modal_ruta)

    def abrir_modal_editar(ruta_item):
        nonlocal id_ruta_edicion
        id_ruta_edicion = obtener_valor(ruta_item, "id", None)

        txt_titulo_modal.value = "Editar ruta"
        txt_nombre_inner.value = str(obtener_valor(ruta_item, "nombre", ""))
        txt_origen_inner.value = str(obtener_valor(ruta_item, "origen", ""))
        txt_destino_inner.value = str(obtener_valor(ruta_item, "destino", ""))
        txt_tiempo_inner.value = str(obtener_valor(ruta_item, "tiempo_estimado", ""))

        tarifa_val = obtener_valor(ruta_item, "tarifa", None)
        txt_tarifa_inner.value = str(tarifa_val) if tarifa_val not in (None, "-") else ""

        obs_val = obtener_valor(ruta_item, "observaciones", None)
        txt_observaciones_inner.value = str(obs_val) if obs_val not in (None, "-") else ""

        abrir_dialogo(modal_ruta)

    # --- MODAL: VER OBSERVACIÓN COMPLETA ---
    def mostrar_observacion(nombre_ruta, observacion):
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
                            f"Observación de {nombre_ruta or 'esta ruta'}",
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

    # --- MODAL: AVISO DE "FORMULARIO INCOMPLETO" AL INGRESAR/EDITAR RUTA ---
    def mostrar_aviso_formulario_incompleto(campos_faltantes):
        texto_campos = ", ".join(campos_faltantes)
        dialogo_aviso = ft.AlertDialog(
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
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#F59E0B", size=42),
                        ft.Text(
                            "Formulario incompleto",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Debes llenar todos los campos obligatorios para poder "
                            f"agregar la ruta. Falta: {texto_campos}.",
                            size=13,
                            color="#475569",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Entendido",
                            bgcolor="#6366F1",
                            color="white",
                            width=200,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                            on_click=lambda e: cerrar_dialogo(dialogo_aviso),
                        ),
                    ],
                ),
            ),
        )
        abrir_dialogo(dialogo_aviso)

    # --- MODAL: AVISO DE "NO SE PUEDE ELIMINAR" (igual que en choferes) ---
    def mostrar_aviso_no_se_puede_eliminar(nombre_ruta, motivo=""):
        dialogo_aviso = ft.AlertDialog(
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
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#F59E0B", size=42),
                        ft.Text(
                            "No se puede eliminar esta ruta",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            motivo
                            or f"\"{nombre_ruta or 'Esta ruta'}\" tiene registros asociados "
                               "(por ejemplo, viajes) y no puede eliminarse.",
                            size=13,
                            color="#475569",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Entendido",
                            bgcolor="#6366F1",
                            color="white",
                            width=200,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                            on_click=lambda e: cerrar_dialogo(dialogo_aviso),
                        ),
                    ],
                ),
            ),
        )
        abrir_dialogo(dialogo_aviso)

    # --- MODAL DE CONFIRMACIÓN DE ELIMINACIÓN ---
    def confirmar_eliminar(id_r, nombre_r=""):
        if id_r is None:
            mostrar_error("No se pudo identificar la ruta a eliminar")
            return

        def borrar_y_cerrar(e):
            print(f"[vista_rutas] Click en Aceptar-eliminar. id_ruta={id_r!r}, dao={'OK' if dao else 'None'}")
            try:
                if not dao:
                    mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
                    cerrar_dialogo(dialogo_eliminar)
                    return

                dao.eliminar(id_r)
                print(f"[vista_rutas] dao.eliminar({id_r!r}) ejecutado sin excepción")
                cargar_datos_tabla()
                cerrar_dialogo(dialogo_eliminar)
                mostrar_exito("Ruta eliminada con éxito")
            except ValueError as ve:
                # Error de negocio esperado (ej. FK violation por viajes asociados).
                # En vez del snackbar simple, mostramos el mismo aviso "no se puede
                # eliminar" que usa la vista de choferes.
                print(f"[vista_rutas] No se pudo eliminar: {ve}")
                cerrar_dialogo(dialogo_eliminar)
                mostrar_aviso_no_se_puede_eliminar(nombre_r, str(ve))
            except Exception:
                print("[vista_rutas] EXCEPCIÓN al eliminar:")
                traceback.print_exc()
                try:
                    cerrar_dialogo(dialogo_eliminar)
                except Exception:
                    pass
                mostrar_error("Ocurrió un error al eliminar la ruta (revisa la consola/terminal)")

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
                            f"¿Estás seguro de eliminar la ruta \"{nombre_r or id_r}\"?",
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

    # --- 4. TABLA Y DATOS DINÁMICOS ---
    tabla_rutas = ft.DataTable(
        bgcolor="white",
        heading_row_color="#EC932F",
        heading_row_height=38,
        data_row_min_height=48,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("ID", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre de la ruta", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Origen", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Destino", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tiempo estimado", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tarifa", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Obs.", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color="white", size=11, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def obtener_valor(item, clave, valor_defecto="-"):
        if isinstance(item, dict):
            valor = item.get(clave)
        else:
            valor = getattr(item, clave, None)
        return valor if valor is not None else valor_defecto

    def cargar_datos_tabla(filtro=""):
        lista = []
        if dao:
            if filtro.strip() and hasattr(dao, "buscar_por_nombre"):
                lista = dao.buscar_por_nombre(filtro)
            elif hasattr(dao, "obtener_todos"):
                lista = dao.obtener_todos()

        filas = []
        for r in lista:
            id_r = obtener_valor(r, "id", None)
            nombre = obtener_valor(r, "nombre", "Sin nombre")
            origen = obtener_valor(r, "origen", "S/N")
            destino = obtener_valor(r, "destino", "S/N")
            tiempo = obtener_valor(r, "tiempo_estimado", "00:00:00")
            tarifa_val = obtener_valor(r, "tarifa", None)
            observaciones_val = obtener_valor(r, "observaciones", None)

            tarifa_texto = f"${tarifa_val}" if tarifa_val not in (None, "-") else "-"

            tiene_observaciones = bool(
                observaciones_val and str(observaciones_val).strip() not in ["", "-", "None"]
            )
            if tiene_observaciones:
                celda_observaciones = ft.Container(
                    tooltip=str(observaciones_val).strip(),
                    on_click=lambda e, n=nombre, obs=str(observaciones_val).strip(): mostrar_observacion(n, obs),
                    content=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED, size=16, color="#6366F1"),
                )
            else:
                celda_observaciones = ft.Text("-", size=11, color="#CBD5E1")

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_r), size=11, color="#1E293B", weight=ft.FontWeight.W_500)),
                        ft.DataCell(ft.Text(str(nombre), size=11, color="#1E293B", weight=ft.FontWeight.W_500)),
                        ft.DataCell(ft.Text(str(origen), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(destino), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(tiempo), size=11, color="#475569")),
                        ft.DataCell(ft.Text(tarifa_texto, size=11, color="#475569")),
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
                                        on_click=lambda e, ruta_item=r: abrir_modal_editar(ruta_item),
                                        content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=13, color="#EC932F"),
                                    ),
                                    ft.Container(
                                        width=24,
                                        height=24,
                                        border=ft.Border.all(1.5, "#EF4444"),
                                        border_radius=12,
                                        alignment=ft.Alignment(0, 0),
                                        tooltip="Eliminar",
                                        on_click=lambda e, i=id_r, n=nombre: confirmar_eliminar(i, n),
                                        content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=13, color="#EF4444"),
                                    ),
                                ],
                                spacing=6,
                            )
                        ),
                    ]
                )
            )
        tabla_rutas.rows = filas
        try:
            page.update()
        except Exception:
            pass

    def al_cambiar_buscador(e):
        cargar_datos_tabla(e.control.value)

    # --- 5. BUSCADOR Y BOTÓN ---
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
                ft.Text("Agregar ruta", color="white", size=12, weight=ft.FontWeight.BOLD),
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
                ft.Text("Rutas", size=22, weight=ft.FontWeight.BOLD, color="#000000"),
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