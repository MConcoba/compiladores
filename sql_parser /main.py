from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from analizator import MetodosArchivo, SQLLexer, SQLParser

objetoAbrir = MetodosArchivo()
lex = SQLLexer()
par = SQLParser()

def insertarContenido():
    limpiarContenido()
    info = objetoAbrir.abrirArchivo()
    txtCargarArchivo.delete("1.0", tk.END)
    txtCargarArchivo.insert(tk.END, info)
    enumerar2()

def obtenerInfo():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    if infoActual == "\n":
        tk.messagebox.showerror("Ningún Archivo Cargado",
                                "Aún no ha cargado o escrito alguna instruccion")
        return
    else:
        objetoAbrir.contenido = infoActual

def analize_file():
    obtenerInfo()
    enumerar()
    #objetoAbrir.analizadorSintactico()
    lexico = lex.lexico(objetoAbrir.contenido)
    txtConvertirArchivo.delete("1.0", tk.END)
    #txtConvertirArchivo.insert(tk.END, lexico)
    insert_table_in_text(txtConvertirArchivo, lexico, 'lex')
    llenarTabla()

def analizador_sint():
    obtenerInfo()
    enumerar()
    parser = par.sintactico(objetoAbrir.contenido)
    txtConvertirArchivo.delete("1.0", tk.END)
    print(parser)
    #txtConvertirArchivo.insert(tk.END, lexico)
    insert_table_in_text(txtConvertirArchivo, parser, 'par' )
    llenarTabla()

def insert_table_in_text(widget, data, type):
    # Crear tabla
    if type == 'lex':
        table_lex = ttk.Treeview(widget, columns=('Token', 'Tipo'), show='headings')
        table_lex.heading('Token', text='Token')
        table_lex.heading('Tipo', text='Tipo')
        table_lex.column(0, width=400)
        table_lex.column(1, width=400)
        # Calcular el ancho máximo de cada columna
        

        # Agregar datos a la tabla
        for key, value in data.items():
            tokens = ', '.join([str(item['token']) for item in value])
            types = ', '.join([item['type'] for item in value])
            table_lex.insert('', 'end', values=(tokens, types))

        # Colocar la tabla dentro del widget de texto
        table_lex.place(x=0, y=0, width=40, height=500)
        table_lex['height']=20
        widget.window_create(tk.END, window=table_lex)
    else:
        table_lex = ttk.Treeview(widget, columns=('Tipo', 'Respuesta'), show='headings')
        table_lex.heading('Tipo', text='Tipo')
        table_lex.heading('Respuesta', text='Respuesta')
        table_lex.column(0, width=400)
        table_lex.column(1, width=400)

        for diccionario in data:
            for clave, valor in diccionario.items():
                print(f"Clave: {clave}, Valor: {valor}")
                table_lex.insert('', 'end', values=(clave, valor))

        # Colocar la tabla dentro del widget de texto
        table_lex.place(x=0, y=0, width=40, height=500)
        table_lex['height']=20
        widget.window_create(tk.END, window=table_lex)


def EstadoExportar():
    if par.listaErrores:
        subMenuTokens.entryconfig("Exportar", state="disabled")
    else:
        subMenuTokens.entryconfig("Exportar", state="normal")

def exportarSQL():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.exportarSQL(infoActual)


def Guardar():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.marcarCambios(infoActual)
    objetoAbrir.guardarArchivo(infoActual)

def guardarComo():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.guardarArchivoComo(infoActual)

def cerrar():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.marcarCambios(infoActual)

    interfaz.protocol("WM_DELETE_WINDOW", 
                      objetoAbrir.cerrarVentana(infoActual,interfaz))

def limpiarContenido():
    txtConvertirArchivo.delete("1.0", tk.END)
    txtCargarArchivo.delete("1.0", tk.END)
    txtlineaNumerica.config(state="normal")
    txtlineaNumerica2.config(state="normal")
    txtlineaNumerica.delete("1.0", tk.END)
    txtlineaNumerica2.delete("1.0", tk.END)
    objetoAbrir.limpiarVariables()
    #tabla.delete(*tabla.get_children())


def enumerar():
    txtlineaNumerica.config(state="normal")
    txtlineaNumerica.delete("1.0", tk.END)

    for i in range(1,objetoAbrir.cantidadLineas+1):
        txtlineaNumerica.insert(tk.END, f"{i}\n")
    txtlineaNumerica.config(state="disabled")

def enumerar2():
    txtlineaNumerica2.config(state="normal")
    txtlineaNumerica2.delete("1.0", tk.END)

    for i in range(1,objetoAbrir.cantidadLineas+1):
        txtlineaNumerica2.insert(tk.END, f"{i}\n")
    txtlineaNumerica2.config(state="disabled")

def llenarTabla():
    #tabla.delete(*tabla.get_children())
    for clave, valor in objetoAbrir.listaErrores.items():
        pass
        #tabla.insert("", "end", values=(clave,valor))
    EstadoExportar()
    objetoAbrir.listaErrores = {}

def colorear_linea(numLinea):
    txtConvertirArchivo.tag_remove("coloreada", "1.0", "end")
    txtCargarArchivo.tag_remove("coloreada", "1.0", "end")

    linea = int(numLinea)
    txtConvertirArchivo.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    txtCargarArchivo.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    txtlineaNumerica.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    txtlineaNumerica2.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    
def seleccionar_fila(event):
    pass
    #item = tabla.selection()[0]  #obtener el índice de la fila seleccionada
    #numero_linea, nombre_error = tabla.item(item, "values")
    #colorear_linea(numero_linea)



interfaz = tk.Tk()
interfaz.title("Automatas")
interfaz.geometry("1366x768")
interfaz.attributes('-fullscreen', True)
interfaz.config(background="white")

barraMenu = tk.Menu(interfaz)

subMenuArchivo = tk.Menu(barraMenu, tearoff=0)
subMenuArchivo.add_command(label="Abrir",command=insertarContenido)
subMenuArchivo.add_command(label="Guardar", command=Guardar)
subMenuArchivo.add_command(label="Guardar como...", command=guardarComo)
subMenuArchivo.add_command(label="Limpiar contenido", command=limpiarContenido)

subMenuTokens = tk.Menu(barraMenu, tearoff=0)
subMenuTokens.add_command(label="Analizador Lexico", command=analize_file) 
subMenuTokens.add_command(label="Analizador Sintactico", command=analizador_sint) 
subMenuTokens.add_command(label="Exportar", command= exportarSQL ,state="disabled")

subMenuSalir = tk.Menu(barraMenu, tearoff=0)
# subMenuSalir.add_command(label="Cerrar Programa",command=interfaz.destroy)  
subMenuSalir.add_command(label="Cerrar Programa",command=cerrar)  

#hago los menus
barraMenu.add_cascade(label="Archivo", menu=subMenuArchivo)
barraMenu.add_cascade(label="Opciones", menu=subMenuTokens)
barraMenu.add_cascade(label="Salir", menu=subMenuSalir)

interfaz.config(menu=barraMenu)

txtCargarArchivo = tk.Text(interfaz, wrap="none", width=78, height=26,font=("Century Gothic", 11),
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtCargarArchivo.place(x= 30, y = 10)
txtCargarArchivo.config(padx=10,pady=10)
txtCargarArchivo.tag_configure("coloreada", background="yellow", foreground="black")


txtConvertirArchivo = tk.Text(interfaz, wrap="none", width=100, height=26, font=("Century Gothic", 11),
                            highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtConvertirArchivo.place(x= 693, y=10)
txtConvertirArchivo.config(padx= 10,pady=10)
#configurar un tag para cambiar el color
txtConvertirArchivo.tag_configure("coloreada", background="yellow", foreground="black")


txtlineaNumerica = tk.Text(interfaz, wrap="none", width=3, height=26,font=("Century Gothic", 11),
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtlineaNumerica.place(x= 673, y=10)
txtlineaNumerica.config(pady=10, fg="red")


txtlineaNumerica2 = tk.Text(interfaz, wrap="none", width=3, height=26,font=("Century Gothic", 11),
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtlineaNumerica2.place(x= 10, y=10)
txtlineaNumerica2.config(pady=10, fg="red")


#sincronizar scroll de cajas
def sincornizar(txtOrigen, txtDestino, txtDestino2, txtDestino3):
    def sincroDesplazamiento(*args):
        fraccion = txtOrigen.yview()[0]
        txtDestino.yview_moveto(fraccion)
        txtDestino2.yview_moveto(fraccion)
        txtDestino3.yview_moveto(fraccion)

    return sincroDesplazamiento

sincroConvertirAlinea = sincornizar(txtConvertirArchivo, txtlineaNumerica, txtCargarArchivo,txtlineaNumerica2)
sincroLineaAconvertir = sincornizar(txtlineaNumerica, txtConvertirArchivo,txtCargarArchivo, txtlineaNumerica2)
sincroCargarLineaConvertir = sincornizar(txtCargarArchivo,txtlineaNumerica, txtConvertirArchivo,txtlineaNumerica2)
sincroLinea2CargarLineaConvertir = sincornizar(txtlineaNumerica2,txtCargarArchivo,txtlineaNumerica, txtConvertirArchivo)

txtConvertirArchivo.config(yscrollcommand=sincroConvertirAlinea)
txtlineaNumerica.config(yscrollcommand=sincroLineaAconvertir)
txtCargarArchivo.config(yscrollcommand=sincroCargarLineaConvertir)
txtlineaNumerica2.config(yscrollcommand=sincroLinea2CargarLineaConvertir)



#inicio de mi tabla
""" tabla = ttk.Treeview(interfaz, columns=("Número de Línea", "Nombre de Error"))
tabla.bind("<<TreeviewSelect>>", seleccionar_fila)  # Asociar evento de selección
tabla['height'] = 7

style = ttk.Style()
style.configure('Treeview', font=("Century Gothic", 11 ), foreground='black' )
style.configure('Treeview.Heading', font=('Century Gothic', 13), foreground='black')

tabla.heading("#1", text="Número de Línea")
tabla.heading("#2", text="Nombre de Error")

tabla.column("#0", width=0)
tabla.column("#1", width=200,anchor="center")
tabla.column("#2", width=1145,anchor="w")


tabla.place(x = 10,y=560) """




interfaz.mainloop()