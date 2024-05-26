import flet as ft
from constranst import theme
from components.menu import menu

def main(page: ft.Page):
    bar = menu(page)
    page = theme(page)
    page.add(ft.Text('Welcome'))
    page.add(bar[0])
    page.update()
    


ft.app(target=main)