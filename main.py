import flet as ft 
from views.viajes import vista_viajes

def main(page: ft.Page):
    page.title = "UniRuta"
    page.window_width = 1400
    page.window_height = 800
    page.window_resizable = True
    page.bgcolor = "#F5F5F5"
    page.padding = 0

    page.add(
        vista_viajes(page)
    )

ft.run(main)