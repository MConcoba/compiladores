import flet as ft

def theme(page: ft.Page):
    page.theme_mode = "dark"
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    #page.window_maximized = True
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.INDIGO,
    )
    page.title = 'Compiladores'

    return page

