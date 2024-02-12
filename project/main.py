import flet as ft
from constranst import theme
from components.menu import menu

def main(page: ft.Page):
    page = theme(page)
    page.add(ft.Text('Welcome'))
    page.add(menu())
    page.update()
    


ft.app(target=main)