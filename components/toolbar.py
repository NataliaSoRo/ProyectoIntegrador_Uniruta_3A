from models.viaje import Viaje
from dao.viaje_dao import ViajeDAO
from dao.unidad_dao import UnidadDAO

import flet as ft

def guardar_viaje(e, page, unidad, chofer, ruta, fecha, hora, estatus):

    origen, destino = ruta.value.split(" - ")

    viaje = Viaje(
        origen=origen,
        destino=destino,
        fecha=fecha.value,
        hora=hora.value,
        estatus=estatus.value,
        unidad=int(unidad.value),
    )

    dao = ViajeDAO()
    dao.insertar_viaje(viaje)

    page.pop_dialog()
    
    page.snack_bar = ft.SnackBar(
        content=ft.Text("Viaje guardado correctamente")
    )
    page.snack_bar.open = True

    page.update()

def abrir_dialogo(e, page):

    unidad_dao = UnidadDAO()
    unidades = unidad_dao.obtener_todos()

    unidad = ft.Dropdown(
        label = "No. Unidad",
        width=300,
        options=[
            ft.dropdown.Option(
                key=str(u.id),
                text=u.noeconomico,
            )
            for u in unidades
        ]
    )

    chofer = ft.Dropdown(
        label="Chofer",
        width=300,
        options=[
            ft.dropdown.Option("Juan Pérez"),
            ft.dropdown.Option("Alan Martinez"),
            ft.dropdown.Option("Carlos Gómez"),
            ft.dropdown.Option("Sofia Ruiz"),
            ft.dropdown.Option("Miguel Ramos"),
        ]
    )

    ruta = ft.Dropdown(
        label="Ruta",
        width=300,
        options=[
            ft.dropdown.Option("Huamantla - Apizaco"),
            ft.dropdown.Option("Terrenate - Huamantla"),
            ft.dropdown.Option("H. Galeana - Huamantla"),
            ft.dropdown.Option("Apizaco - Xalpatlahuaya"),
            ft.dropdown.Option("Contla - Xalpatlahuaya"),
        ]
    )

    fecha = ft.TextField(
        label="Fecha",
        hint_text="dd/mm/aaaa",
        width=300,
    )

    hora = ft.TextField(
        label="Hora de salida",
        hint_text="00:00",
        width=300,
    )

    hora_llegada = ft.TextField(
    label="Hora de llegada",
    hint_text="00:00",
    width=300,
)

    pasajeros = ft.TextField(
        label="Pasajeros",
        hint_text="Ejemplo: 25",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    observaciones = ft.TextField(
        label="Observaciones",
        width=300,
        multiline=True,
        min_lines=2,
        max_lines=3,
    )

    estatus = ft.Dropdown(
        label="Estatus",
        width=300,
        options=[
            ft.dropdown.Option("En curso"),
            ft.dropdown.Option("Concluido"),
            ft.dropdown.Option("Inactivo"),
        ]
    )

    dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Programar viaje"),
        content=ft.Column(
            tight=True,
            spacing=15,
            controls=[
                unidad,
                chofer,
                ruta,
                fecha,
                hora,
                hora_llegada,
                pasajeros,
                observaciones,
                estatus, 
            ]
        ),

        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: page.pop_dialog(),
            ),

            ft.ElevatedButton(
                "Guardar",
                on_click=lambda e: guardar_viaje(
                    e,
                    page,
                    unidad,
                    chofer,
                    ruta,
                    fecha,
                    hora,
                    estatus,
                ),
            ),
        ],
    )

    page.show_dialog(dialogo)

def toolbar(page):

    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

        controls=[

            ft.Container(

                width=350,

                content=ft.TextField(
                    hint_text="Buscar viaje...",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=12,
                    filled=True,
                    bgcolor="white",
                ),
            ),

            ft.ElevatedButton(

                "Programar viaje",

                icon=ft.Icons.ADD,

                bgcolor="white",

                on_click=lambda e: abrir_dialogo(e, page),

                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=20,
                ),
            ),
        ],
    )