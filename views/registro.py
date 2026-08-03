from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario
import flet as ft

def vista_registro(page: ft.Page, ir_a):  
    # --- CAMPOS DE ENTRADA ---
    txt_nombre = ft.TextField(
        label="Nombre completo",
        hint_text="ej. Juan Ramos Alcaraz",
        filled=True,
        bgcolor="#F3F4F6",
        border_radius=8,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color="#3B82F6",
    )

    txt_email = ft.TextField(
        label="Correo electronico",
        hint_text="ej. juanpez123@gmail.com",
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
    )

    # --- LÓGICA DE REGISTRO ---
    def procesar_registro(e):
        nombre = txt_nombre.value.strip()
        correo = txt_email.value.strip()
        contrasena = txt_password.value.strip()
        confirmar = txt_confirm_password.value.strip()

        if not nombre or not correo or not contrasena or not confirmar:
            page.open(
                ft.SnackBar(
                    ft.Text("Por favor, llena todos los campos"),
                    bgcolor="orange"
                )
            )
            return

        if contrasena != confirmar:
            page.open(
                ft.SnackBar(
                    ft.Text("Las contraseñas no coinciden"),
                    bgcolor="red"
                )
            )
            return

        try:
            dao = UsuarioDAO()
            nuevo_id = dao.obtener_ultimo_id() + 1
            
            nuevo_usuario = Usuario(
                id=nuevo_id,
                nombre=nombre,
                correo=correo,
                contrasena=contrasena,
                rol="usuario"
            )

            dao.registrar(nuevo_usuario)

            page.open(
                ft.SnackBar(
                    ft.Text("¡Registro exitoso! Por favor inicia sesión"),
                    bgcolor="green"
                )
            )
            ir_a("login")

        except Exception as ex:
            print("Error al registrar:", ex)
            page.open(
                ft.SnackBar(
                    ft.Text("Error al guardar el usuario en la base de datos"),
                    bgcolor="red"
                )
            )

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

    # --- TEXTO CON LÍNEA "BIENVENIDO AL SISTEMA DE UNIRUTA" ---
    seccion_bienvenida = ft.Container(
        top=180,
        left=210,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                # Línea horizontal azul encima del texto
                ft.Container(
                    width=280,
                    height=3,
                    bgcolor="#2B5B84"
                ),
                ft.Text(
                    "Bienvenido al\nsistema de\nUNIRUTA", 
                    size=42, 
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

    # --- TARJETA DE REGISTRO ---
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
                        "Registrate", 
                        size=22, 
                        weight=ft.FontWeight.BOLD, 
                        color="#1B2559"
                    )
                ),
                txt_nombre,
                txt_email,
                txt_password,
                txt_confirm_password,
                ft.Container(height=5), # Espaciador pequeño
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
                            content=ft.Text("Iniciar sesión", size=11, color="#3B82F6", weight=ft.FontWeight.BOLD),
                            on_click=lambda e: ir_a("login"), # 👈 Te regresa directo a Iniciar Sesión
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
                card_registro,
                icono_bus_esquina,
            ]
        ),
    )