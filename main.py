
import sys
from pathlib import Path
import flet as ft

sys.path.append(str(Path(__file__).resolve().parent))

from views.choferes import vista_choferes
from views.iniciarsesion import vista_login
from views.menu_principal import vista_menu_principal
from views.pagos import vista_pagos
from views.registro import vista_registro
from views.rutas import vista_rutas
from views.unidades import vista_unidades
from views.viajes import vista_viajes
from views.vista_perfil import vista_perfil


def main(page: ft.Page):
    page.title = "UniRuta"
    page.window.width = 1200
    page.window.height = 700
    page.window.resizable = True
    page.padding = 0

    page.ruta_actual = "login"

    def ir_a(ruta):
        ruta_previa = page.ruta_actual

        if ruta != "perfil":
            page.ruta_actual = ruta

        page.controls.clear()

        if ruta == "login":
            page.add(vista_login(page, ir_a))
        elif ruta == "registro":
            page.add(vista_registro(page, ir_a))
        elif ruta == "menu_principal":
            page.add(vista_menu_principal(page, ir_a))
        elif ruta == "viajes":
            page.add(vista_viajes(page, ir_a))
        elif ruta == "choferes":
            page.add(vista_choferes(page, ir_a))
        elif ruta == "unidades": 
            page.add(vista_unidades(page, ir_a))
        elif ruta == "rutas":
            page.add(vista_rutas(page, ir_a))
        elif ruta == "pagos":
            page.add(vista_pagos(page, ir_a))
        elif ruta == "perfil":
            page.add(vista_perfil(page, ir_a, ruta_previa=ruta_previa))

        page.update()

    # Si quieres probar directo la pantalla de unidades al iniciar, usa ir_a("unidades")
    ir_a("login")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")