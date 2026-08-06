import re
import flet as ft
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario


def vista_registro(page: ft.Page, ir_a):
    dao = UsuarioDAO()

    def limpiar_errores(e=None):
        txt_nombre.error_text = None
        txt_email.error_text = None
        txt_password.error_text = None
        txt_confirm_password.error_text = None
        page.update()

    txt_nombre = ft.TextField(
        label="Nombre completo",
        hint_text="ej. Juan Ramos Alcaraz",
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
        on_change=limpiar_errores,
    )

    txt_email = ft.TextField(
        label="Correo electronico",
        hint_text="ej. juanpez123@gmail.com",
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
        on_change=limpiar_errores,
    )

    txt_password = ft.TextField(
        label="Contraseña",
        hint_text="Mínimo 8 caracteres",
        password=True,
        can_reveal_password=True,
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
        on_change=limpiar_errores,
    )

    txt_confirm_password = ft.TextField(
        label="Confirmar contraseña",
        hint_text="••••••••",
        password=True,
        can_reveal_password=True,
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
        on_change=limpiar_errores,
    )

    def mostrar_snack(mensaje, color):
        snack = ft.SnackBar(content=ft.Text(mensaje), bgcolor=color)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def validar_formulario(nombre, correo, contrasena, confirmar):
        valido = True
        errores = []

        if not nombre:
            txt_nombre.error_text = "Ingresa tu nombre completo"
            errores.append("Falta el nombre completo")
            valido = False
        elif len(nombre) < 3:
            txt_nombre.error_text = "El nombre debe tener al menos 3 caracteres"
            errores.append("El nombre es demasiado corto")
            valido = False

        patron_correo = r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$"
        if not correo:
            txt_email.error_text = "Ingresa tu correo electrónico"
            errores.append("Falta el correo electrónico")
            valido = False
        elif not re.match(patron_correo, correo):
            txt_email.error_text = "Correo no válido (ej. nombre@dominio.com)"
            errores.append("El correo no tiene un formato válido")
            valido = False

        if not contrasena:
            txt_password.error_text = "Ingresa una contraseña"
            errores.append("Falta la contraseña")
            valido = False
        elif len(contrasena) < 8:
            txt_password.error_text = "Debe tener al menos 8 caracteres"
            errores.append("La contraseña debe tener al menos 8 caracteres")
            valido = False

        if not confirmar:
            txt_confirm_password.error_text = "Confirma tu contraseña"
            errores.append("Falta confirmar la contraseña")
            valido = False
        elif contrasena and confirmar and contrasena != confirmar:
            txt_confirm_password.error_text = "Las contraseñas no coinciden"
            errores.append("Las contraseñas no coinciden")
            valido = False

        page.update()
        return valido, errores

    def procesar_registro(e):
        print("=== CLIC EN REGISTRARME DETECTADO ===")
        limpiar_errores()

        nombre = (txt_nombre.value or "").strip()
        correo = (txt_email.value or "").strip().lower()
        contrasena = (txt_password.value or "").strip()
        confirmar = (txt_confirm_password.value or "").strip()

        # Diagnóstico SIN exponer la contraseña real
        patron_correo_diag = r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$"
        correo_es_valido = bool(re.match(patron_correo_diag, correo))
        print(
            f"nombre={nombre!r} | correo={correo!r} | "
            f"len_pass={len(contrasena)} | len_confirm={len(confirmar)} | "
            f"coinciden={contrasena == confirmar} | "
            f"correo_valido={correo_es_valido}"
        )

        valido, errores = validar_formulario(nombre, correo, contrasena, confirmar)
        if not valido:
            print("Validación falló:", errores)
            mostrar_snack(" | ".join(errores), "red")
            return

        try:
            print("Verificando si el correo ya existe...")
            if dao.correo_existe(correo):
                txt_email.error_text = "Ese correo ya está registrado"
                mostrar_snack("Ese correo ya está registrado", "red")
                page.update()
                return

            print("Registrando usuario...")
            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                contrasena=contrasena,
                rol="usuario",
            )
            dao.registrar(nuevo_usuario)
            print("Usuario registrado correctamente")

            usuario_logueado = dao.login(correo, contrasena)
            if usuario_logueado is not None:
                page.usuario_actual = usuario_logueado
                mostrar_snack(f"¡Bienvenido {usuario_logueado.nombre}!", "green")
                ir_a("menu_principal")
            else:
                mostrar_snack("Registro exitoso. Por favor inicia sesión.", "green")
                ir_a("login")

        except Exception as ex:
            print("!!! ERROR AL REGISTRAR:", repr(ex))
            mensaje_error = str(ex).lower()
            if "duplicate" in mensaje_error or "unique" in mensaje_error:
                txt_email.error_text = "Ese correo ya está registrado"
                page.update()
                mostrar_snack("Ese correo ya está registrado", "red")
            elif "correo" in mensaje_error:
                mostrar_snack("El correo no se pudo guardar correctamente", "red")
            else:
                mostrar_snack("No se pudo completar el registro. Verifica los datos e intenta de nuevo.", "red")

    logo_uniruta = ft.Container(
        top=25,
        left=30,
        content=ft.Image(src="logo_uniruta.png", width=130, fit="contain"),
    )

    seccion_bienvenida = ft.Container(
        top=180,
        left=210,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Container(width=280, height=3, bgcolor="#2B5B84"),
                ft.Text(
                    "Bienvenido al\nsistema de\nUNIRUTA",
                    size=42,
                    weight=ft.FontWeight.NORMAL,
                    color="#2C3E50",
                ),
            ],
        ),
    )

    ilustracion_personajes = ft.Container(
        left=30,
        bottom=20,
        content=ft.Image(src="bailarines.png", width=360, fit="contain"),
    )

    card_registro = ft.Container(
        top=140,
        right=260,
        width=380,
        padding=30,
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.12, "black"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            spacing=14,
            controls=[
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "Registrate", size=22, weight=ft.FontWeight.BOLD, color="#1B2559"
                    ),
                ),
                txt_nombre,
                txt_email,
                txt_password,
                txt_confirm_password,
                ft.Container(height=5),
                ft.ElevatedButton(
                    "Registrarme",
                    bgcolor="#3B82F6",
                    color="white",
                    width=380,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=procesar_registro,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("¿Ya tienes una cuenta?", size=11, color="grey"),
                        ft.TextButton(
                            content=ft.Text(
                                "Iniciar sesión",
                                size=11,
                                color="#3B82F6",
                                weight=ft.FontWeight.BOLD,
                            ),
                            on_click=lambda e: ir_a("login"),
                        ),
                    ],
                ),
            ],
        ),
    )

    circulo_inferior_izq = ft.Container(
        width=650, height=650, bgcolor="#52A1C1", border_radius=325, left=-180, bottom=-180
    )
    circulo_superior_der = ft.Container(
        width=650, height=650, bgcolor="#7CBAD0", border_radius=325, right=-100, top=-100
    )
    icono_bus_esquina = ft.Container(
        right=30, bottom=20, content=ft.Icon(ft.Icons.DIRECTIONS_BUS, size=45, color="#94A3B8")
    )

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
                card_registro,
                icono_bus_esquina,
            ]
        ),
    )