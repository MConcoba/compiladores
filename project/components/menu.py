import flet as ft
from views.squres_code import pick_file, analize, export
import os

# Obtener la ruta actual
ruta_actual = os.getcwd()
ruta_file = None
codigo_archivo = None
def menu(page: ft.Page):
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        global ruta_file
        if  e.files != None:
            ruta_file = e.files[0].path.replace(".txt", ".sql")
            file = pick_file(e, page)
            page.add(file)

    
    def result(e):
       result = analize(page)
       page.add(result)
    
    
    def save_file_result(e: ft.FilePickerResultEvent):
        global codigo_archivo
        name = f"{e.path}.sql"
        with open(name, "w") as f:
            f.write(export())
        
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    save_file_dialog = ft.FilePicker(on_result=save_file_result)


    menu =  ft.AppBar(
        leading=ft.Icon(ft.icons.CODE),
        leading_width=70,
        title=ft.Text("Analizador Lexico"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        elevation=100,
        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.FOLDER_ROUNDED,
                 tooltip='Archivo',
                items=[
                    ft.PopupMenuItem(icon=ft.icons.FILE_OPEN_ROUNDED, text="Abrir   Ctrl+O", 
                    on_click=lambda _: pick_files_dialog.pick_files( initial_directory=ruta_actual, allowed_extensions=["txt"], allow_multiple=False
                    ),),
                    ft.PopupMenuItem(icon=ft.icons.SAVE_ROUNDED, text="Exportar (.sql)", on_click=lambda _: save_file_dialog.save_file( 
                        initial_directory=ruta_file+'.sql', allowed_extensions=['sql']
                    ),),
                ], 
            ),
            ft.PopupMenuButton(
                icon=ft.icons.GENERATING_TOKENS_ROUNDED,
                 tooltip='Tokens',
                items=[
                    ft.PopupMenuItem(icon=ft.icons.PLAY_CIRCLE_ROUNDED, text="Analizar   Ctrl+T", on_click=result),
                ],
            ),
        ],
    )
    return [menu, pick_files_dialog, save_file_dialog]