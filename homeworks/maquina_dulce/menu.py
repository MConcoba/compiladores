import flet as ft
from maquina_dulce.read_code import show_code
from maquina_dulce.afd_dulce import get_lines

code = None
codigo_archivo = None
def menu(page: ft.Page):
    selected_files = ft.Text()

    def pick_files_result(e: ft.FilePickerResultEvent):
        global code, codigo_archivo
        with open(e.files[0].path, 'r', encoding='utf-8') as archivo:
            codigo_archivo = archivo.read()
        code = show_code(page, codigo_archivo, '', '', False, False, False)
        page.add(code)
    
    def result(e):
        global code, codigo_archivo
        if codigo_archivo is None:
            return
        else:
            page.remove(code)
            automata = get_lines(codigo_archivo)
            code = show_code(page, codigo_archivo, automata[0], '', False, False, False)
            page.add(code)
        
        
    #print(selected_files)
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

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
                    ft.PopupMenuItem(icon=ft.icons.FILE_OPEN_ROUNDED, text="Abrir   Ctrl+O", 
                                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),),
                    ft.PopupMenuItem(icon=ft.icons.SAVE_ROUNDED, text="Resultados", on_click=result),
                    #ft.PopupMenuItem(icon=ft.icons.SAVE_ROUNDED, text="Guardar  Ctrl+S"),
                    #ft.PopupMenuItem(icon=ft.icons.SAVE_AS_ROUNDED, text="Guardar como  Ctrl+Shift+S"),
                    #ft.PopupMenuItem(icon=ft.icons.CLOSE_ROUNDED, text="Cerrar  Alt+F4"),
                ], 
            ),
        ],
    )
    return [menu, pick_files_dialog, code]