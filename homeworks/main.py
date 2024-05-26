import flet as ft
from maquina_dulce.menu import menu

def main(page: ft.Page):
    page.theme_mode = "light"
    bar = menu(page)
    page.add(bar[0])
    page.overlay.extend([bar[1]])

    page.update()
    


ft.app(target=main)