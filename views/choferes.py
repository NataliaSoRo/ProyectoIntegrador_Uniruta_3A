import flet as ft
from datetime import datetime
import traceback
import unicodedata

try:
    from dao.chofer_dao import ChoferDAO
    from models.chofer import Chofer
except ImportError as ex:
    print(f"[vista_choferes] ERROR al importar ChoferDAO/Chofer: {ex}")
    ChoferDAO = None
    Chofer = None


def normalizar_texto(texto):
    """Quita espacios, mayúsculas y acentos para comparar de forma segura."""
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    return texto


# ==========================================
# VISTA CHOFERES (COMPLETA Y COMPATIBLE)
# ==========================================
def vista_choferes(page: ft.Page, ir_a):
    page.title = "UniRuta - Choferes"

    dao = ChoferDAO() if ChoferDAO else None

    # Variables de estado para controlar si editamos o creamos
    id_chofer_edicion = None

    # Usuario de sesión
    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = getattr(usuario, "nombre", "Natalia Sosa Rodriguez") if usuario else "Natalia Sosa Rodriguez"
    rol_usuario = getattr(usuario, "rol", "Administrador") if usuario else "Administrador"
    correo_usuario = getattr(usuario, "correo", getattr(usuario, "email", "usuario@uniruta.com")) if usuario else "usuario@uniruta.com"

    # --- DATEPICKER (VIGENCIA) ---
    def al_cambiar_fecha(e):
        if date_picker.value:
            txt_vigencia_inner.value = date_picker.value.strftime("%Y-%m-%d")
            txt_vigencia_inner.update()

    date_picker = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2040, 12, 31),
        on_change=al_cambiar_fecha,
    )

    if date_picker not in page.overlay:
        page.overlay.append(date_picker)

    def abrir_calendario(e):
        abrir_dialogo(date_picker)

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
        try:
            snack_exito.content.controls[1].value = mensaje
            snack_exito.bgcolor = "#10B981"
            snack_exito.content.controls[0].name = ft.Icons.CHECK_CIRCLE
            _mostrar_snack()
        except Exception as ex:
            print(f"[vista_choferes] Error al mostrar snackbar de éxito: {ex}")
            traceback.print_exc()

    def mostrar_error(mensaje):
        try:
            snack_exito.content.controls[1].value = mensaje
            snack_exito.bgcolor = "#EF4444"
            snack_exito.content.controls[0].name = ft.Icons.ERROR_OUTLINE
            _mostrar_snack()
        except Exception as ex:
            print(f"[vista_choferes] Error al mostrar snackbar de error: {ex}")
            traceback.print_exc()

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
                item_sidebar("Choferes", ft.Icons.BADGE_OUTLINED, "choferes", activo=True),
                item_sidebar("Unidades", ft.Icons.DIRECTIONS_BUS_OUTLINED, "unidades"),
                item_sidebar("Rutas", ft.Icons.MAP_OUTLINED, "rutas"),
                item_sidebar("Viajes", ft.Icons.WORK_OUTLINE, "viajes"),
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
            ],
        ),
    )

    # --- COMPONENTES DEL FORMULARIO Y MODAL ---
    txt_titulo_modal = ft.Text("Ingresar chofer", size=22, weight=ft.FontWeight.BOLD, color="#0F172A")

    txt_foto_inner = ft.TextField(
        hint_text="EJ. foto_chofer.png",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )
    txt_foto = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_foto_inner,
    )

    txt_nombre_inner = ft.TextField(
        hint_text="EJ. Carlos Mendoza Ruiz",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )
    txt_nombre = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_nombre_inner,
    )

    dd_tipo_licencia_inner = ft.Dropdown(
        hint_text="Seleccionar tipo",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        options=[
            ft.dropdown.Option("Estatal tipo A"),
            ft.dropdown.Option("Estatal tipo B"),
            ft.dropdown.Option("Federal tipo A"),
            ft.dropdown.Option("Federal tipo B"),
        ],
        expand=True,
    )
    dd_tipo_licencia = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=dd_tipo_licencia_inner,
    )

    txt_vigencia_inner = ft.TextField(
        hint_text="EJ. 2028-05-15",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        read_only=True,
        suffix_icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_calendario,
        expand=True,
    )
    txt_vigencia = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_vigencia_inner,
        on_click=abrir_calendario,
    )

    txt_telefono_inner = ft.TextField(
        hint_text="EJ. 2411029384",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )
    txt_telefono = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_telefono_inner,
    )

    txt_no_licencia_inner = ft.TextField(
        hint_text="EJ. LIC-10293",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        expand=True,
    )
    txt_no_licencia = ft.Container(
        height=40,
        bgcolor="#F8FAFC",
        border=ft.Border.all(1, "#CBD5E1"),
        border_radius=8,
        alignment=ft.Alignment(-1, 0),
        content=txt_no_licencia_inner,
    )

    dd_estatus_inner = ft.Dropdown(
        hint_text="Seleccionar estatus",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        value="Activo",
        options=[
            ft.dropdown.Option("Activo"),
            ft.dropdown.Option("Inactivo"),
            ft.dropdown.Option("Licencia"),
            ft.dropdown.Option("Dado de baja"),
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

    txt_observaciones_inner = ft.TextField(
        hint_text="EJ. Cubre turno nocturno, sin restricciones",
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
        alignment=ft.Alignment(-1, -1),
        content=txt_observaciones_inner,
    )

    def restablecer_formulario():
        nonlocal id_chofer_edicion
        id_chofer_edicion = None
        txt_titulo_modal.value = "Ingresar chofer"
        txt_foto_inner.value = ""
        txt_nombre_inner.value = ""
        dd_tipo_licencia_inner.value = None
        txt_vigencia_inner.value = ""
        txt_telefono_inner.value = ""
        txt_no_licencia_inner.value = ""
        dd_estatus_inner.value = "Activo"
        txt_observaciones_inner.value = ""

    def guardar_chofer(e):
        nonlocal id_chofer_edicion

        print("[vista_choferes] guardar_chofer: click en Aceptar")

        if not txt_nombre_inner.value or not str(txt_nombre_inner.value).strip():
            mostrar_error("El nombre completo es obligatorio")
            return
        if not txt_no_licencia_inner.value or not str(txt_no_licencia_inner.value).strip():
            mostrar_error("El número de licencia es obligatorio")
            return
        if not dd_tipo_licencia_inner.value:
            mostrar_error("Selecciona el tipo de licencia")
            return
        if not txt_vigencia_inner.value:
            mostrar_error("Selecciona la vigencia de la licencia")
            return
        if not txt_telefono_inner.value or not str(txt_telefono_inner.value).strip():
            mostrar_error("El teléfono es obligatorio")
            return
        if not dd_estatus_inner.value:
            mostrar_error("Selecciona el estatus del chofer")
            return

        if not Chofer or not dao:
            mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
            return

        observaciones_valor = (
            str(txt_observaciones_inner.value).strip()
            if txt_observaciones_inner.value and str(txt_observaciones_inner.value).strip()
            else None
        )

        chofer_obj = Chofer(
            id=id_chofer_edicion,
            nombre=str(txt_nombre_inner.value).strip(),
            telefono=str(txt_telefono_inner.value).strip(),
            licencia=str(txt_no_licencia_inner.value).strip(),
            tipo_licencia=dd_tipo_licencia_inner.value,
            vigen_licencia=txt_vigencia_inner.value,
            foto=txt_foto_inner.value if txt_foto_inner.value else None,
            estatus=dd_estatus_inner.value,
            observaciones=observaciones_valor,
        )

        mensaje = ""

        try:
            if id_chofer_edicion is None:
                dao.insertar(chofer_obj)
                mensaje = "Chofer ingresado con éxito"
            else:
                dao.actualizar(chofer_obj)
                mensaje = "Chofer actualizado con éxito"
            print(f"[vista_choferes] guardar_chofer: guardado en BD OK -> {mensaje}")
        except Exception:
            print(f"[vista_choferes] ERROR al guardar/actualizar en BD:")
            traceback.print_exc()
            mostrar_error("Ocurrió un error al guardar el chofer (revisa la consola/terminal)")
            return

        try:
            restablecer_formulario()
            cerrar_dialogo(modal_agregar)
            cargar_datos_tabla()
            print("[vista_choferes] guardar_chofer: UI refrescada OK")
        except Exception:
            print(f"[vista_choferes] ERROR al refrescar la UI tras guardar:")
            traceback.print_exc()

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
                                ft.Text("Ruta/Nombre de Imagen", size=11, color="#475569"),
                                txt_foto,
                                ft.Text("No. licencia", size=11, color="#475569"),
                                txt_no_licencia,
                                ft.Text("Estatus", size=11, color="#475569"),
                                dd_estatus,
                            ],
                        ),
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Nombre completo", size=11, color="#475569"),
                                txt_nombre,
                                ft.Text("Tipo de licencia", size=11, color="#475569"),
                                dd_tipo_licencia,
                                ft.Text("Vigencia", size=11, color="#475569"),
                                txt_vigencia,
                                ft.Text("Teléfono", size=11, color="#475569"),
                                txt_telefono,
                            ],
                        ),
                    ],
                ),
                ft.Text("Observaciones", size=11, color="#475569"),
                txt_observaciones,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Aceptar", bgcolor="#6366F1", color="white", expand=True, on_click=guardar_chofer),
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

    def abrir_modal_editar(chofer_item):
        nonlocal id_chofer_edicion
        id_chofer_edicion = obtener_valor(chofer_item, "id")

        txt_titulo_modal.value = "Editar chofer"
        txt_nombre_inner.value = str(obtener_valor(chofer_item, "nombre", ""))
        txt_telefono_inner.value = str(obtener_valor(chofer_item, "telefono", ""))
        txt_no_licencia_inner.value = str(obtener_valor(chofer_item, "licencia", ""))
        dd_tipo_licencia_inner.value = obtener_valor(chofer_item, "tipo_licencia", None)
        txt_vigencia_inner.value = str(obtener_valor(chofer_item, "vigen_licencia", ""))

        foto_val = obtener_valor(chofer_item, "foto", "")
        txt_foto_inner.value = str(foto_val) if foto_val else ""

        dd_estatus_inner.value = str(obtener_valor(chofer_item, "estatus", "Activo"))

        observaciones_val = obtener_valor(chofer_item, "observaciones", "")
        txt_observaciones_inner.value = str(observaciones_val) if observaciones_val else ""

        try:
            date_picker.value = datetime.strptime(txt_vigencia_inner.value, "%Y-%m-%d")
        except (ValueError, TypeError):
            date_picker.value = None

        abrir_dialogo(modal_agregar)

    def mostrar_aviso_no_se_puede_eliminar(nombre_chofer, estatus_chofer):
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
                            "No se puede eliminar este chofer",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color="#0F172A",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            f"{nombre_chofer or 'Este chofer'} tiene estatus "
                            f"\"{estatus_chofer or '-'}\". Solo se pueden eliminar "
                            f"choferes con estatus \"Dado de baja\".",
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

    def mostrar_observacion(nombre_chofer, observacion):
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
                            f"Observación de {nombre_chofer or 'este chofer'}",
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

    # --- MODAL DE CONFIRMACIÓN DE ELIMINACIÓN ---
    def confirmar_eliminar(id_chofer, nombre_chofer="", estatus_chofer=""):
        if id_chofer is None:
            mostrar_error("No se pudo identificar al chofer a eliminar")
            return

        # Comparación robusta: quita espacios, mayúsculas y acentos, para que
        # variaciones como "Dado De Baja", " dado de baja ", "dado de baja"
        # o incluso "dado de bája" (typo con acento) sí se reconozcan.
        estatus_norm = normalizar_texto(estatus_chofer)

        print(
            f"[vista_choferes] confirmar_eliminar -> id={id_chofer!r}, "
            f"nombre={nombre_chofer!r}, estatus_original={estatus_chofer!r}, "
            f"estatus_normalizado={estatus_norm!r}"
        )

        if estatus_norm != "dado de baja":
            mostrar_aviso_no_se_puede_eliminar(nombre_chofer, estatus_chofer)
            return

        def borrar_y_cerrar(e):
            print(f"[vista_choferes] Click en Aceptar-eliminar. id_chofer={id_chofer!r}, dao={'OK' if dao else 'None'}")
            try:
                if not dao:
                    mostrar_error("No hay conexión con la base de datos (revisa la consola/terminal)")
                    cerrar_dialogo(dialogo_eliminar)
                    return

                dao.eliminar(id_chofer)
                print(f"[vista_choferes] dao.eliminar({id_chofer!r}) ejecutado sin excepción")
            except ValueError as ve:
                print(f"[vista_choferes] No se pudo eliminar: {ve}")
                cerrar_dialogo(dialogo_eliminar)
                mostrar_error(str(ve))
                return
            except Exception:
                print("[vista_choferes] EXCEPCIÓN al eliminar en BD:")
                traceback.print_exc()
                try:
                    cerrar_dialogo(dialogo_eliminar)
                except Exception:
                    pass
                mostrar_error("Ocurrió un error al eliminar el chofer (revisa la consola/terminal)")
                return

            try:
                cerrar_dialogo(dialogo_eliminar)
                cargar_datos_tabla()
                print("[vista_choferes] borrar_y_cerrar: UI refrescada OK")
            except Exception:
                print("[vista_choferes] ERROR al refrescar la UI tras eliminar:")
                traceback.print_exc()

            mostrar_exito("Chofer eliminado con éxito")

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
                            "¿Estas seguro de eliminar este registro de chofer?",
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

    # --- TABLA Y BUSCADOR ---
    txt_buscar = ft.TextField(
        hint_text="EJ. Carlos Mendoza",
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 0, 10, 0),
        text_size=12,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: cargar_datos_tabla(e.control.value or ""),
    )

    container_buscar = ft.Container(
        width=450,
        height=38,
        bgcolor="white",
        border=ft.Border.all(1, "#E2E8F0"),
        border_radius=20,
        content=txt_buscar,
    )

    tabla_choferes = ft.DataTable(
        bgcolor="white",
        heading_row_color="#EC932F",
        heading_row_height=42,
        data_row_min_height=52,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text("NO.", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre del chofer", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Teléfono", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("No. Licencia", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo de licencia", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Vigencia de licencia", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Obs.", color="white", size=11, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color="white", size=11, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def obtener_valor(item, clave, valor_defecto="-"):
        if isinstance(item, dict):
            return item.get(clave) or valor_defecto
        return getattr(item, clave, valor_defecto) or valor_defecto

    def color_por_estatus(estatus_str):
        e = estatus_str.strip().lower()
        if e in ("activo", "disponible"):
            return "#10B981"
        if e == "licencia":
            return "#F59E0B"
        if e == "dado de baja":
            return "#EF4444"
        return "#64748B"

    def cargar_datos_tabla(filtro=""):
        filtro = filtro or ""

        lista = []
        if dao:
            try:
                if filtro.strip() and hasattr(dao, "buscar_por_nombre"):
                    lista = dao.buscar_por_nombre(filtro)
                elif hasattr(dao, "obtener_todos"):
                    lista = dao.obtener_todos()
            except Exception:
                print(f"[vista_choferes] Error al cargar datos de la tabla:")
                traceback.print_exc()
                lista = []

        lista = lista or []

        filas = []
        for idx, c in enumerate(lista, start=1):
            id_ch = obtener_valor(c, "id", None)
            nombre_ch = obtener_valor(c, "nombre", "")
            telefono_ch = obtener_valor(c, "telefono", "-")
            licencia_ch = obtener_valor(c, "licencia", "-")
            tipo_lic_ch = obtener_valor(c, "tipo_licencia", "-")
            vigen_lic_ch = obtener_valor(c, "vigen_licencia", "-")
            foto_ch = obtener_valor(c, "foto", None)
            estatus_str = str(obtener_valor(c, "estatus", "Activo"))
            observaciones_ch = obtener_valor(c, "observaciones", None)

            color_est = color_por_estatus(estatus_str)

            tiene_observaciones = bool(observaciones_ch and str(observaciones_ch).strip() not in ["", "-", "None"])
            if tiene_observaciones:
                celda_observaciones = ft.Container(
                    tooltip=str(observaciones_ch).strip(),
                    on_click=lambda e, n=nombre_ch, obs=str(observaciones_ch).strip(): mostrar_observacion(n, obs),
                    content=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED, size=16, color="#6366F1"),
                )
            else:
                celda_observaciones = ft.Text("-", size=11, color="#CBD5E1")

            if foto_ch and str(foto_ch) not in ["-", "None", ""]:
                avatar_content = ft.Image(src=str(foto_ch), fit=ft.BoxFit.COVER)
            else:
                avatar_content = ft.Icon(ft.Icons.PERSON, size=14, color="white")

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(idx), size=11, color="#1E293B")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=avatar_content,
                                        bgcolor="#94A3B8",
                                        radius=14,
                                    ),
                                    ft.Text(str(nombre_ch), size=11, color="#1E293B", weight=ft.FontWeight.W_500),
                                ],
                                spacing=8,
                            )
                        ),
                        ft.DataCell(ft.Text(str(telefono_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(licencia_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(tipo_lic_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(str(vigen_lic_ch), size=11, color="#475569")),
                        ft.DataCell(ft.Text(estatus_str, size=11, color=color_est, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(celda_observaciones),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.Container(
                                        width=26,
                                        height=26,
                                        border=ft.Border.all(1.5, "#EC932F"),
                                        border_radius=13,
                                        alignment=ft.Alignment(0, 0),
                                        tooltip="Editar",
                                        on_click=lambda e, chofer_item=c: abrir_modal_editar(chofer_item),
                                        content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=14, color="#EC932F"),
                                    ),
                                    ft.Container(
                                        width=26,
                                        height=26,
                                        border=ft.Border.all(1.5, "#EF4444"),
                                        border_radius=13,
                                        alignment=ft.Alignment(0, 0),
                                        tooltip="Eliminar",
                                        on_click=lambda e, i=id_ch, n=nombre_ch, est=estatus_str: confirmar_eliminar(i, n, est),
                                        content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=14, color="#EF4444"),
                                    ),
                                ],
                                spacing=8,
                            )
                        ),
                    ]
                )
            )
        tabla_choferes.rows = filas
        try:
            page.update()
        except Exception:
            pass

    btn_ingresar = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="white", size=16), ft.Text("Ingresar chofer", color="white", size=12)],
            tight=True,
            spacing=4,
        ),
        bgcolor="#EC932F",
        on_click=abrir_modal_agregar,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
    )

    cargar_datos_tabla()

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
                    ft.Container(
                        expand=True,
                        padding=30,
                        content=ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Choferes", size=26, weight=ft.FontWeight.BOLD, color="#0F172A"),
                                ft.Container(height=10),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[container_buscar, btn_ingresar],
                                    spacing=15,
                                ),
                                ft.Container(height=20),
                                ft.Container(
                                    border_radius=12,
                                    shadow=ft.BoxShadow(blur_radius=10, color="#1A000000", offset=ft.Offset(0, 4)),
                                    content=tabla_choferes,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )