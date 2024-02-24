import flet as ft


def square(page: ft.Page, code, edit, type, char):
    div = ft.Column(
        spacing=10,
        height=page.window_height-190,
        scroll=ft.ScrollMode.ADAPTIVE,        
    )

    def button_clicked(his, token, result):
        print(token)

    if char == True:
        for e in code:
            div.controls.append(
                ft.TextButton(
                    content=ft.Container(
                        content=ft.Column(
                            [ft.Text(value=e[1]),],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                            width=page.window_width-100
                        ),
                        padding=ft.padding.all(10),
                    ),
                    #on_click=button_clicked, data=e
                    on_click=lambda e, his=e[2], t=e[4], res=e[0]: button_clicked(his, t, res)
                ),
            )

    elif type == 'Text' and not char:
        texto = '\n'.join(code)
        div.controls = [ft.Text(texto, font_family='Consolas', color=ft.colors.RED, size=16)]
    else:
        div.controls = [ft.TextField(value=code, multiline=True, disabled=False, )]

    return div

dlg_modal = None
def show_code(page: ft.Page, code, token, errors, e_code, e_tokens, char):
    #texto = '\n'.join(errors)
    lista_de_errores = errors
    print(lista_de_errores)
   
    cl = square(page, code, e_code, 'Code', False)
    c2 = square(page, token, e_tokens, 'Code', False)
    #c3 = square(page, lista_de_errores, True, 'Text', char)

    

    code = ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                cl,
                padding=5,
                col={"sm": 6, "md": 6, "xl": 6},
                border=ft.border.all(2, ft.colors.BLACK),
                height=page.window_height-100
            ),
           
            ft.Container(
                ft.Stack(
                    [
                        #ft.IconButton(icon="info", right=0),
                        c2,
                        ft.IconButton(
                            width=35,
                            icon=ft.icons.INFO_OUTLINE,
                            icon_color="blue400",
                            icon_size=25,
                            tooltip="Informacion",
                            right=0,
                            
                        ),
                        #c2
                    ]
                ),
                padding=5,
                col={"sm": 6, "md": 6, "xl": 6},
                border=ft.border.all(2, ft.colors.BLACK),
                height=page.window_height-100
            )
        ]),
    ])

    return code
