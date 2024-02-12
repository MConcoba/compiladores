import flet as ft

def menu():
    menu =  ft.AppBar(
        leading=ft.Icon(ft.icons.CODE),
        leading_width=70,
        title=ft.Text("Analizador Léxico "),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        elevation=100,
        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.FOLDER_ROUNDED,
                 tooltip='Archivo',
                items=[
                    ft.PopupMenuItem(icon=ft.icons.FILE_OPEN_ROUNDED, text="Abrir   Ctrl+O"),
                    ft.PopupMenuItem(icon=ft.icons.SAVE_ROUNDED, text="Guardar  Ctrl+S"),
                    ft.PopupMenuItem(icon=ft.icons.SAVE_AS_ROUNDED, text="Guardar como  Ctrl+Shift+S"),
                    ft.PopupMenuItem(icon=ft.icons.CLOSE_ROUNDED, text="Cerrar  Alt+F4"),
                ], 
            ),
        ],
    )
    return menu