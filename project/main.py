import flet as ft
from constranst import theme
from components.menu import menu

def main(page: ft.Page):

    page = theme(page)
    #page.add(ft.Text('Welcome'))
    bar = menu(page)
    page.add(bar[0])
    page.overlay.extend([bar[1]])
        
    page.update()
    


ft.app(target=main)