import flet as ft
from controllers.sqlparser import analizadorSintactico

code = None
codigo_archivo = None

def detalle_row(page, row):
        text = 'Error:' if row['status'] == False else 'Mensaje:'
        dlg_modal = ft.AlertDialog(
        title=ft.Text("Dellate consulta",  weight=ft.FontWeight.W_900,),
        content=ft.Column([ 
            ft.ListView(expand=True, spacing=10, controls=[
                ft.Text("Consulta: ", size=15, 
                spans=[
                    ft.TextSpan(row['token']),
                ]
            ),
            ft.Text(text, size=15, 
                selectable=True,
                spans=[
                    ft.TextSpan(row['menssage'], ft.TextStyle(italic=True, size=16, color=ft.colors.BLUE),),
                ]
            ),
            ]),
            
        ], height=250, width=250),        
        )
        
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

def pick_file(event, page):
        global code, codigo_archivo
        if codigo_archivo is not None:
            page.remove(code)
        
        with open(event.files[0].path, 'r', encoding='utf-8') as archivo:
            codigo_archivo = archivo.read()
        code = show_code(page, codigo_archivo, 'null', True)
        #print(code)
        return code
        page.add(code)

def analize(page):
        global code, codigo_archivo
        if codigo_archivo is None:
            return
        else:
            page.remove(code)
            parse = analizadorSintactico(codigo_archivo)
            code = show_code(page, codigo_archivo, parse, False)
            #print(code)
            return code

def lisata_c():
        columnas = ['No.', 'Toknes', 'Mensaje', 'Estado']
        lista = []
        for c in columnas:
            col = ft.DataColumn(
                ft.Text(c),
            )
            lista.append(col)
        return lista

def lista_r(page, datos):
    lista = []
    for c in datos:
        #print(c)
        row = ft.DataRow([
                ft.DataCell(ft.Text(c['query'])),
                ft.DataCell(ft.Text(c['token'])),
                ft.DataCell(ft.Text(c['menssage'])),
                ft.DataCell(ft.Text(c['status']))
        ],  color="0x30FF0000" if c['status'] == False else {"hovered": "BLUE50"}, on_select_changed=lambda e, value=c: detalle_row(page, value),)
        lista.append(row)
    return lista

def tbl_results(page: ft.page, res):
    #print(res)
    if res != 'null' :
        tbl =   ft.DataTable(
                border=ft.border.all(4, "black"),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, "black"),
                horizontal_lines=ft.border.BorderSide(1, "black"),
                heading_row_color=ft.colors.BLACK12,
                data_row_color={"hovered": "0x30FF0000"},
                columns = lisata_c(),
                rows= lista_r(page, res)
            ),
        return tbl
    else:
        div = ft.Column(
        spacing=10,
        height=page.window_height-190,
        scroll=ft.ScrollMode.ADAPTIVE,        
    )
        return div


def square(page: ft.Page, code, res, edit, type):
    div = ft.Column(
        spacing=10,
        height=page.window_height-190,
        scroll=ft.ScrollMode.ADAPTIVE,        
    )

    if type == 'res':
        if  res != 'null':
            div.controls = tbl_results(page, res)
        else:
            div.controls = [ft.Text('Analiza el contenido')]
    else:
        div.controls = [ft.TextField(value=code, multiline=True, disabled=edit, )]

    return div

dlg_modal = None
def show_code(page: ft.Page, code, results, type):
    cl = square(page, code, results, False, 'code')
    c2 = square(page, code, results, False, 'res')

    code = ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                cl,
                padding=5,
                col={"sm": 6, "md": 6, "xl": 6},
                border=ft.border.all(2, ft.colors.BLACK),
                height=page.window_height-10
            ),
           
            ft.Container(
                ft.Stack(
                    [c2]
                ),
                padding=5,
                col={"sm": 6, "md": 6, "xl": 6},
                border=ft.border.all(2, ft.colors.BLACK),
                height=page.window_height-10
            )
        ]),
    ])

    return code
