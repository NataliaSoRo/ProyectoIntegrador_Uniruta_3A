import flet as ft
from dao.kpi_dao import KpiDAO
import traceback


def vista_ganancias(page: ft.Page, ir_a):
    page.title = "UniRuta - Ganancias"

    dao = KpiDAO()

    usuario = getattr(page, "usuario_actual", None)
    nombre_usuario = getattr(usuario, "nombre", "Administrador") if usuario else "Administrador"
    rol_usuario = getattr(usuario, "rol", "Administrador") if usuario else "Administrador"

    # --- HEADER ---
    def cerrar_sesion(e):
        if hasattr(page, "usuario_actual"):
            page.usuario_actual = None
        ir_a("login")

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

    # --- SIDEBAR ---
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
                    ft.Text(texto, color=color_txt, size=13,
                             weight=(ft.FontWeight.BOLD if activo else ft.FontWeight.W_500)),
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
                item_sidebar("Pagos", ft.Icons.ATTACH_MONEY, "pagos"),
                item_sidebar("Ganancias", ft.Icons.BAR_CHART_ROUNDED, "ganancias", activo=True),
            ],
        ),
    )

    # --- TARJETA KPI DE GANANCIA TOTAL ---
    txt_ganancia_total = ft.Text("$0.00", size=28, weight=ft.FontWeight.BOLD, color="#0F172A")

    tarjeta_total = ft.Container(
        bgcolor="white",
        border_radius=12,
        padding=ft.Padding(20, 16, 20, 16),
        width=260,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 3),
        ),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(ft.Icons.ATTACH_MONEY, color="#10B981", size=22),
                        ft.Text("Ganancias totales", size=13, color="#64748B", weight=ft.FontWeight.W_500),
                    ],
                ),
                txt_ganancia_total,
            ],
        ),
    )

    # --- GRÁFICA DE BARRAS HECHA A MANO (sin flet_charts) ---
    ALTURA_MAX_BARRA = 240  # px del contenedor más alto
    COLORES_BARRAS = ["#EC932F", "#0E4A5B", "#6366F1", "#10B981", "#F97316", "#0284C7"]

    fila_barras = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=24,
        scroll=ft.ScrollMode.AUTO,
        controls=[],
    )

    contenedor_grafica = ft.Container(
        bgcolor="white",
        border_radius=12,
        padding=20,
        expand=True,
        height=380,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 3),
        ),
        content=ft.Column(
            expand=True,
            spacing=10,
            controls=[
                ft.Text("Ganancia por ruta", size=15, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Container(
                    height=ALTURA_MAX_BARRA + 60,
                    padding=ft.Padding(10, 10, 10, 0),
                    content=fila_barras,
                ),
            ],
        ),
    )

    msg_sin_datos = ft.Text(
        "Aún no hay viajes con pasajeros y tarifa registrados para calcular ganancias.",
        size=12,
        color="#94A3B8",
        visible=False,
    )

    def construir_barra(nombre_ruta, ganancia, color, max_valor):
        # Altura proporcional al valor más grande del conjunto
        if max_valor > 0:
            altura_px = max(6, int((ganancia / max_valor) * ALTURA_MAX_BARRA))
        else:
            altura_px = 6

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Text(f"${ganancia:,.2f}", size=10, color="#334155", weight=ft.FontWeight.W_500),
                ft.Container(
                    width=42,
                    height=altura_px,
                    bgcolor=color,
                    border_radius=ft.BorderRadius(6, 6, 0, 0),
                    tooltip=f"{nombre_ruta}: ${ganancia:,.2f}",
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                ),
                ft.Container(
                    width=70,
                    content=ft.Text(
                        str(nombre_ruta),
                        size=10,
                        color="#475569",
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ),
            ],
        )

    def cargar_datos():
        try:
            resumen = dao.obtener_resumen_kpis()
            ganancia_total = resumen.get("ganancias_totales", 0.0) or 0.0
            txt_ganancia_total.value = f"${ganancia_total:,.2f}"

            datos_ruta = dao.obtener_ganancias_por_ruta()
        except Exception:
            print("[vista_ganancias] Error al cargar datos:")
            traceback.print_exc()
            datos_ruta = []

        fila_barras.controls.clear()

        if not datos_ruta:
            msg_sin_datos.visible = True
        else:
            msg_sin_datos.visible = False
            valores = [float(g or 0) for (_nombre, g) in datos_ruta]
            max_valor = max(valores) if valores else 0

            for i, (nombre_ruta, ganancia) in enumerate(datos_ruta):
                ganancia_f = float(ganancia or 0)
                color = COLORES_BARRAS[i % len(COLORES_BARRAS)]
                fila_barras.controls.append(
                    construir_barra(nombre_ruta, ganancia_f, color, max_valor)
                )

        try:
            page.update()
        except Exception:
            pass

    cargar_datos()

    area_trabajo = ft.Container(
        expand=True,
        bgcolor="#FAFAFA",
        padding=ft.Padding(25, 15, 25, 20),
        content=ft.Column(
            expand=True,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Ganancias", size=24, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Row(controls=[tarjeta_total]),
                msg_sin_datos,
                contenedor_grafica,
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