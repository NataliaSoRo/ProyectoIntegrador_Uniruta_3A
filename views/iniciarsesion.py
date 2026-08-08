from dao.usuario_dao import UsuarioDAO
import flet as ft

def vista_login(page: ft.Page, ir_a):
    # --- CAMPOS DE ENTRADA ---
    txt_email = ft.TextField(
        label="Correo electronico",
        hint_text="ej. juanpez234@gmail.com",
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
    )

    txt_password = ft.TextField(
        label="Contraseña",
        hint_text="••••••••",
        password=True,
        can_reveal_password=True,
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
    )

    # --- LÓGICA DE LOGIN ---
    def procesar_login(e):
        # Normalizamos igual que en el registro: sin espacios y correo en minúsculas
        correo = (txt_email.value or "").strip().lower()
        contrasena = (txt_password.value or "").strip()

        print(f"[LOGIN] Intentando con correo={correo!r} | longitud_contrasena={len(contrasena)}")

        if not correo or not contrasena:
            snack = ft.SnackBar(
                content=ft.Text("Por favor, llena todos los campos"),
                bgcolor="orange"
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return

        try:
            dao = UsuarioDAO()
            usuario = dao.login(correo, contrasena)

            if usuario is not None:
                print(f"[LOGIN] Éxito. Usuario id={usuario.id}, nombre={usuario.nombre}")

                # Guardamos el objeto usuario directamente en el objeto page (100% compatible)
                page.usuario_actual = usuario

                snack = ft.SnackBar(
                    content=ft.Text(f"Bienvenido {usuario.nombre}"),
                    bgcolor="green"
                )
                page.overlay.append(snack)
                snack.open = True
                page.update()

                # Redirección al Menú Principal
                ir_a("menu_principal")
            else:
                print("[LOGIN] Falló: dao.login() devolvió None (correo no existe o contraseña no coincide)")
                snack = ft.SnackBar(
                    content=ft.Text("Correo o contraseña incorrectos"),
                    bgcolor="red"
                )
                page.overlay.append(snack)
                snack.open = True
                page.update()

        except Exception as ex:
            print("[LOGIN] Error en login:", repr(ex))
            snack = ft.SnackBar(
                content=ft.Text("Error al conectar con la base de datos"),
                bgcolor="red"
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()

    # --- LOGO (Esquina superior izquierda) ---
    logo_uniruta = ft.Container(
        top=25,
        left=30,
        content=ft.Image(
            src="logo_uniruta.png",
            width=130,
            fit="contain"
        )
    )

    # --- TEXTO "BIENVENIDO DE NUEVO!" ---
    seccion_bienvenida = ft.Container(
        top=180,
        left=210,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Container(
                    width=280,
                    height=3,
                    bgcolor="#2B5B84"
                ),
                ft.Text(
                    "Bienvenido de\nnuevo!",
                    size=48,
                    weight=ft.FontWeight.NORMAL,
                    color="#2C3E50"
                )
            ]
        )
    )

    # --- ILUSTRACIÓN DE BAILARINES ---
    ilustracion_personajes = ft.Container(
        left=30,
        bottom=20,
        content=ft.Image(
            src="bailarines.png",
            width=360,
            fit="contain"
        )
    )

    # --- TARJETA DE LOGIN ---
    card_login = ft.Container(
        top=160,
        right=260,
        width=380,
        padding=35,
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.12, "black"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            spacing=18,
            controls=[
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "Iniciar sesión",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#1B2559"
                    )
                ),
                txt_email,
                txt_password,
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Checkbox(
                            label="Recordarme",
                            value=False,
                            fill_color={
                                ft.ControlState.DEFAULT: "white",
                                ft.ControlState.SELECTED: "#3B82F6",
                            },
                            check_color="white",
                            border_side=ft.BorderSide(2, "#3B82F6"),
                        ),
                        ft.TextButton(
                            content=ft.Text("¿Olvidaste tu contraseña?", size=11, color="#3B82F6"),
                            on_click=lambda e: print("Olvido contraseña"),
                        ),
                    ],
                ),
                ft.ElevatedButton(
                    "Iniciar sesión",
                    bgcolor="#3B82F6",
                    color="white",
                    width=380,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=procesar_login,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("¿No tienes una cuenta?", size=11, color="grey"),
                        ft.TextButton(
                            content=ft.Text("Registrarme", size=11, color="#3B82F6", weight=ft.FontWeight.BOLD),
                            on_click=lambda e: ir_a("registro"),
                        ),
                    ],
                ),
            ],
        ),
    )

    # --- CÍRCULOS Y DETALLES DE FONDO ---
    circulo_inferior_izq = ft.Container(
        width=650,
        height=650,
        bgcolor="#52A1C1",
        border_radius=325,
        left=-180,
        bottom=-180
    )
    circulo_superior_der = ft.Container(
        width=650,
        height=650,
        bgcolor="#7CBAD0",
        border_radius=325,
        right=-100,
        top=-100
    )
    icono_bus_esquina = ft.Container(
        right=30,
        bottom=20,
        content=ft.Icon(ft.Icons.DIRECTIONS_BUS, size=45, color="#94A3B8")
    )

    # --- ESTRUCTURA PRINCIPAL ---
    return ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Stack(
            controls=[
                circulo_inferior_izq,
                circulo_superior_der,
                logo_uniruta,
                seccion_bienvenida,
                ilustracion_personajes,
                card_login,
                icono_bus_esquina,
            ]
        ),
    )