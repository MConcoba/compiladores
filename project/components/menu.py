import flet as ft
from views.squres_code import pick_file, analize

code = None
codigo_archivo = None
def menu(page: ft.Page):
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        file = pick_file(e, page)
        page.add(file)

    
    def result(e):
       result = analize(page)
       page.add(result)
        
        
    #print(selected_files)
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

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
                                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),),
                    ft.PopupMenuItem(icon=ft.icons.SAVE_ROUNDED, text="Exportar (.sql)", on_click=result),
                ], 
            ),
            ft.PopupMenuButton(
                icon=ft.icons.GENERATING_TOKENS_ROUNDED,
                 tooltip='Tokens',
                items=[
                    ft.PopupMenuItem(icon=ft.icons.PLAY_CIRCLE_ROUNDED, text="Analizar   Ctrl+T"),
                ],
            ),
        ],
    )
    return [menu, pick_files_dialog, code]