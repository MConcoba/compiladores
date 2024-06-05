import flet as ft

def main(page: ft.Page):
    page.theme_mode = "light"

    def detalle_row(row):
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

    def lisata_c():
        columnas = ['No.', 'Toknes', 'Mensaje', 'Estado']
        lista = []
        for c in columnas:
            col = ft.DataColumn(
                ft.Text(c),
            )
            lista.append(col)
        return lista

    def lista_r():
        rows = [{'query': 1, 'token': ['CREATEDATABASE', 'mi_base_de_datos', 'fas', ';'], 'menssage': '1-Error de sintaxis: se encontró fas, se esperaba ;', 'status': False}, {'query': 2, 'token': ['CREATETABLE', 'empleados', '(', 'id', 'INT', 'PRIMARY', 'KEY', ',', 'nombre', 'VARCHAR', '(', '50', '),', 'edad', 'INT', ',', 'puesto', 'VARCHAR', '(', '50', '),', 'salario', 'DECIMAL', '(', '10', ',', '2', ')', ')', ';'], 'menssage': 'Consulta aceptada', 'status': True}, {'query': 3, 'token': ['SELECT', 'nombre', ',', 'edad', 'FROM', 'empleados', ';'], 'menssage': 'Consulta aceptada', 'status': True}, {'query': 4, 'token': ['SELECT', 'FROM', 'empleados', 'WHERE', 'edad', '>', '30', ';'], 'menssage': 'Consulta aceptada', 'status': True}, {'query': 5, 'token': ['INSERTINTO', 'empleados', '(', 'nombre', ',', 'edad', ',', 'puesto', ')', 'VALUES', '(', "'Juan", "Pérez'", ',', '28', ',', "'Desarrollador'", ')', ';'], 'menssage': 'Consulta aceptada', 'status': True}, {'query': 6, 'token': ['UPDATE', 'empleados', 'SET', 'edad', '=', '29', 'WHERE', 'nombre', '=', 'Juan', ';'], 'menssage': 'Consulta aceptada', 'status': True}, {'query': 7, 'token': ['DELETEFROM', 'empleados', 'WHERE', 'edad', '<', '25', ';'], 'menssage': 'Consulta aceptada', 'status': True}]

        lista = []
        for c in rows:
            row = ft.DataRow([
                    ft.DataCell(ft.Text(c['query'])),
                    ft.DataCell(ft.Text(c['token'])),
                    ft.DataCell(ft.Text(c['menssage'])),
                    ft.DataCell(ft.Text(c['status']))
            ],  color="0x30FF0000" if c['status'] == False else {"hovered": "BLUE50"}, on_select_changed=lambda e, value=c: detalle_row(value),
)
            lista.append(row)
        return lista

    page.add(
        ft.DataTable(
            border=ft.border.all(4, "black"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, "black"),
            horizontal_lines=ft.border.BorderSide(1, "black"),
            heading_row_color=ft.colors.BLACK12,
            data_row_color={"hovered": "0x30FF0000"},
            columns = lisata_c(),
            rows= lista_r()
        
        ),
    )

ft.app(target=main)