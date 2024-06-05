import flet as ft
from controllers.sqlparser import analizadorSintactico
from controllers.lexer import lexico
from controllers.parser import sintactico
code = None
codigo_archivo = None

dlg_modal = None

def export():
    return code.controls[0].controls[0].content.controls[0].value

def pick_file(event, page):
        global code, codigo_archivo
        if codigo_archivo is not None:
            page.remove(code)
        
        with open(event.files[0].path, 'r', encoding='utf-8') as archivo:
            codigo_archivo = archivo.read()
        code = show_code(page, codigo_archivo, 'null', True, False)
        return code

def detalle_row(page, row, lex):
        label1 = ''
        label2 = ''
        value1 = ''
        value2 = ''
        if lex:
            label1 = 'Tokens: \n'
            value1 = row['tokens']
        else:
            label1 = 'Consulta: \n' if row['status'] else 'Nota: \n'
            value1 = row['tipo']
            label2 = 'Respuesta: \n'
            value2 = f"{row['tipo']} {row['datos']}"  if row['status'] else row['datos']

        
        dlg_modal = ft.AlertDialog(
        title=ft.Text("Detalle consulta \n \n", size=35, weight=ft.FontWeight.W_900,),
        content = ft.Column([ 
            ft.ListView(expand=True, spacing=20, controls=[
                ft.Text(label1, italic=False, size=25, weight=ft.FontWeight.W_800,
                    spans=[ft.TextSpan(value1, ft.TextStyle(
                         size=20, color=ft.colors.GREEN ))]),
                ft.Text(label2, size=25, selectable=True, weight=ft.FontWeight.W_800,
                    spans=[ft.TextSpan(value2, 
                    ft.TextStyle(size=20, color=ft.colors.BLUE))]),
            ]),
        ], 
        height=350, width=450))
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

def analize(page, lex):
        global code, codigo_archivo
        if codigo_archivo is None:
            return
        else:
            page.remove(code)
            last = code.controls[0].controls[0].content.controls[0].value
            if lex :     
                analized = lexico(last)
            else:
                analized = sintactico(last)     
            
            code = show_code(page, last, analized, False, lex)
            #print(code)
            return code

def lisata_c(lex):
        columnas = ['No.', 'Tokens' ] if lex else ['Tipo', 'Respueta', 'Estado']
        lista = []
        for c in columnas:
            col = ft.DataColumn(
                ft.Text(c),
            )
            lista.append(col)
        return lista

def lista_r(page, datos, lex):
    lista = []
    if lex:
        for c in datos:
            row = ft.DataRow([
                    ft.DataCell(ft.Text(c['query'])),
                    ft.DataCell(ft.Text(str(c['tokens']))),
            ], color={"hovered": "BLUE50"},  on_select_changed=lambda e, value=c: detalle_row(page, value, lex))
            lista.append(row)
    else:
        print(datos)
        for c in datos:
            row = ft.DataRow([
                    ft.DataCell(ft.Text(str(c['tipo']))),
                    ft.DataCell(ft.Text(str(c['datos']))),
                    ft.DataCell(ft.Text(c['status']))
            ],  color="0x30FF0000" if c['status'] == False else {"hovered": "BLUE50"}, on_select_changed=lambda e, value=c: detalle_row(page, value, lex),)
            lista.append(row)
    return lista

def tbl_results(page: ft.page, res, lex):
    #print(res)
    if res != 'null' :
        tbl =   ft.DataTable(
                border=ft.border.all(4, "black"),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, "black"),
                horizontal_lines=ft.border.BorderSide(1, "black"),
                heading_row_color=ft.colors.BLACK12,
                data_row_color={"hovered": "0x30FF0000"},
                data_row_min_height=90,
                data_row_max_height=100,
                columns = lisata_c(lex),
                rows= lista_r(page, res, lex)
            ),
        return tbl
    else:
        div = ft.Column(
        spacing=10,
        height=page.window_height-190,
        scroll=ft.ScrollMode.ADAPTIVE,        
    )
        return div

def square(page: ft.Page, code, res, edit, type, lex):
    div = ft.Column(
        spacing=10,
        height=page.window_height,
        scroll=ft.ScrollMode.ADAPTIVE,        
    )

    if type == 'res':
        if  res != 'null':
            div.controls = tbl_results(page, res, lex)
        else:
            div.controls = [ft.Text('Analiza el contenido')]
    else:
        div.controls = [ft.TextField(value=code, multiline=True, disabled=edit, )]

    return div

def show_code(page: ft.Page, code, results, type, lex):
    cl = square(page, code, results, False, 'code', lex)
    c2 = square(page, code, results, False, 'res', lex)

    code = ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                cl,
                padding=5,
                col={"sm": 6, "md": 6, "xl": 6},
                border=ft.border.all(2, ft.colors.BLACK),
                height=page.window_height
            ),
           
            ft.Container(
                ft.Stack(
                    [c2]
                ),
                padding=5,
                col={"sm": 6, "md": 6, "xl": 6},
                border=ft.border.all(2, ft.colors.BLACK),
                height=page.window_height
            )
        ]),
    ])

    return code
