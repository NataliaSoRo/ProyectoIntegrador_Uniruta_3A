from dao.viaje_dao import ViajeDAO
import flet as ft

def tabla_viajes():

    dao = ViajeDAO()
    viajes = dao.obtener_todos()

    return ft.DataTable(
        bgcolor="white",
        border_radius=12,
        heading_row_color="#F5B800",

        columns=[
            ft.DataColumn(ft.Text("No. Viaje")),
            ft.DataColumn(ft.Text("No. Unidad")),
            ft.DataColumn(ft.Text("Chofer asignado")),
            ft.DataColumn(ft.Text("Ruta")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora de salida")),
            ft.DataColumn(ft.Text("Estatus")),
            ft.DataColumn(ft.Text("Acciones")),
        ],

        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(viaje.id))),
                    ft.DataCell(ft.Text(str(viaje.id_unidad))),
                    ft.DataCell(ft.Text(getattr(viaje, 'chofer_nombre', None) or "Sin asignar")),
                    ft.DataCell(ft.Text(getattr(viaje, 'ruta_nombre', None) or f"{viaje.origen} - {viaje.destino}")),
                    ft.DataCell(ft.Text(str(viaje.fecha))),
                    ft.DataCell(ft.Text(str(viaje.hora))),
                    ft.DataCell(ft.Text(viaje.estatus)),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda e, viaje=viaje: print(viaje.id),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, viaje=viaje: print(viaje.id),
                                ),
                            ]
                        )
                    ),
                ]
            )
            for viaje in viajes
        ],
    )