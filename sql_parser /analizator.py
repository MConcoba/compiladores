import tkinter as tk
from tkinter import filedialog

import ply.yacc as yacc
import ply.lex as lex

class MetodosArchivo:
    def __init__(self):

        self.contenido = "\n"
        self.listaErrores = {}
        self.cantidadLineas = 0

        self.cambiosRealizados = False
        self.direccionArchivo = None 
        
    def limpiarVariables(self):
        self.contenido = ""
        self.errores = ""
        self.listaErrores = {}
        self.cantidadLineas = 0

    def abrirArchivo(self):
        direccionArchivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if direccionArchivo:
            with open(direccionArchivo, 'r') as archivo:
                contenido = archivo.read()
            self.direccionArchivo = direccionArchivo
            self.cambiosRealizados = False
            self.vacio = False
            self.cantidadLineas = len(contenido.splitlines())

        return contenido
    
    def marcarCambios(self, contenidoCaja):
        if self.contenido != contenidoCaja:
            self.cambiosRealizados = True 
        else:
            self.cambiosRealizados = False

    def cerrarVentana(self,contenidoCaja,ventana):
        contenido = contenidoCaja
        ventana = ventana

        if self.cambiosRealizados:
            respuesta = tk.messagebox.askyesnocancel("Guardar Cambios", "Deseas guardar los cambios antes de cerrar?")
            if respuesta is None:
                return
            elif respuesta:
                self.guardarArchivo(contenido)
        ventana.destroy()

    def guardarArchivoComo(self,contenidoCaja):
        direccionArchivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if direccionArchivo:
            contenido = contenidoCaja
            with open(direccionArchivo, "w") as archivo:
                archivo.write(contenido)
            self.direccionArchivo = direccionArchivo
            self.cambiosRealizados = False

    def guardarArchivo(self, contenidoCaja):
        if self.direccionArchivo:
            contenido = contenidoCaja
            with open(self.direccionArchivo, "w") as archivo:
                archivo.write(contenido)
            self.cambiosRealizados = False
        else:
            contenido = contenidoCaja
            self.guardarArchivoComo(contenido)

 
    def exportarSQL(self, contenido):
        archivo = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
    
        if archivo:
            # Guardar el contenido formateado en un archivo .sql
            with open(archivo, 'w') as f:
                f.write(contenido)
            
            tk.messagebox.showinfo("Correcto", "El archivo se ha exportado correctamente")
    
class SQLLexer:
    tokens = (
        'SELECT', 'FROM', 'WHERE', 'ID', 'NUMBER', 'COMMA', 'EQUALS', 'INSERT', 'INTO', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'DATABASE', 'TABLE', 'INDEX','INT','VARCHAR', 'DATE', 'FLOAT', 'TEXT', 'BOOLEAN', 'LPAREN', 'RPAREN','SEMICOLON', 'STRING', 'VALUES', 'SET', 'ON','OR', 'AND', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INTEGER', 'BIGINT', 'REAL', 'DOUBLE', 'DECIMAL','NUMERIC', 'TIME', 'DATETIME', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT', 'PLUS','MINUS', 'TIMES', 'SIMPLEQUOTE', 'DOUBLEQUOTE', 'DIVIDE', 'NOT', 'LESSTHAN', 'GREATERTHAN', 'SERIAL', 'NOTNULL', 'NULL', 'AUTO_INCREMENT', 'PRIMARYKEY', "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "OUTER", "POINT", 'COMPARISON'
    )

    t_COMMA = r','
    t_POINT = r'\.'
    t_EQUALS = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_DOUBLEQUOTE = r'"'
    t_SIMPLEQUOTE = r'\''
    t_GREATERTHAN = r'\>'
    t_LESSTHAN = r'\<'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_CREATE(self, t):
        r'CREATE'
        return t

    def t_DATABASE(self, t):
        r'DATABASE'
        return t

    def t_INDEX(self, t):
        r'INDEX'
        return t

    def t_TABLE(self, t):
        r'TABLE'
        return t

    def t_SELECT(self, t):
        r'SELECT'
        return t

    def t_FROM(self, t):
        r'FROM'
        return t

    def t_WHERE(self, t):
        r'WHERE'
        return t

    def t_INSERT(self, t):
        r'INSERT'
        return t

    def t_INTO(self, t):
        r'INTO'
        return t

    def t_VALUES(self, t):
        r'VALUES'
        return t

    def t_UPDATE(self, t):
        r'UPDATE'
        return t

    def t_SET(self, t):
        r'SET'
        return t

    def t_DELETE(self, t):
        r'DELETE'
        return t

    def t_DROP(self, t):
        r'DROP'
        return t

    def t_ASC(self, t):
        r'ASC'
        return t

    def t_DESC(self, t):
        r'DESC'
        return t

    def t_EXISTS(self, t):
        r'EXISTS'
        return t

    def t_NOTNULL(self, t):
        r'NOTNULL'
        return t

    def t_NULL(self, t):
        r'NULL'
        return t

    def t_AUTOI_NCREMENT(self, t):
        r'AUTO_INCREMENT'
        return t

    def t_PRIMARYKEY(self, t):
        r'PRIMARYKEY'
        return t

    def t_PRIMARY(self, t):
        r'PRIMARY'
        return t

    def t_ORDERBY(self, t):
        r'ORDERBY'
        return t

    def t_GROUPBY(self, t):
        r'GROUPBY'
        return t

    def t_AND(self, t):
        r'AND'
        return t

    def t_OR(self, t):
        r'OR'
        return t

    def t_NOT(self, t):
        r'NOT'
        return t

    def t_ISNULL(self, t):
        r'ISNULL'
        return t

    def t_ISNOTNULL(self, t):
        r'ISNOTNULL'
        return t

    def t_INT(self, t):
        r'INT'
        return t

    def t_VARCHAR(self, t):
        r'VARCHAR'
        return t

    def t_DECIMAL(self, t):
        r'DECIMAL'
        return t

    def t_ON(self, t):
        r'ON'
        return t

    def t_JOIN(self, t):
        r'JOIN'
        return t

    def t_INNER(self, t):
        r'INNER'
        return t

    def t_LEFT(self, t):
        r'LEFT'
        return t

    def t_RIGHT(self, t):
        r'RIGHT'
        return t

    def t_FULL(self, t):
        r'FULL'
        return t

    def t_OUTER(self, t):
        r'OUTER'
        return t


    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)  # Convertir el valor a entero
        return t

    def t_COMPARISON(self, t):
        r'==|<=|>=|<|>|!='
        return t

    # Ignorar espacios en blanco y saltos de línea
    t_ignore = ' \t\n'

    # Definición de errores
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def tokenize(self, input_string):
        self.lexer.input(input_string)
        tokens = []
        line_number = 1  # Inicializamos el número de línea en 1
        current_position = 0  # Inicializamos la posición actual en 0
        for tok in self.lexer:
            if tok.lexpos > current_position: 
                line_number += input_string[current_position:tok.lexpos].count('\n')
            current_position = tok.lexpos
            tok.lineno = line_number  # Asignamos el número de línea al token
            tokens.append(tok)
        return tokens

    def lexico(self, constulas):
        token_dict = {}
        for token in self.tokenize(constulas):
            if token.lineno not in token_dict:
                token_dict[token.lineno] = []
            token_dict[token.lineno].append({'token': token.value, 'type': token.type})
        return token_dict


class SQLParser:
    tokens = SQLLexer.tokens

    def __init__(self):
        self.lexer = SQLLexer()
        self.parser = yacc.yacc(module=self)
        self.listaErrores = []
    
    def parse_sql(self, input_string):
        return self.parser.parse(input_string)
    
    # Definición de la gramática
    def p_statement(self, p):
        '''
        statement : select_statement
                | create_statement
                | insert_statement
                | update_statement
                | delete_statement
                | drop_statement
        '''
        p[0] = p[1]


    def p_select_statement(self, p):
        '''
        select_statement : SELECT column_list FROM table_reference SEMICOLON
                        | SELECT column_list FROM table_reference join_clause SEMICOLON
                        | SELECT column_list FROM table_reference where_clause SEMICOLON
                        | SELECT column_list FROM table_reference join_clause where_clause SEMICOLON
        '''
        if len(p) == 6:
            p[0] = ('SELECT', p[2], 'FROM', p[4], p[5])
        elif len(p) == 7:
            p[0] = ('SELECT', p[2], 'FROM', p[4], p[5], p[6])
        else:
            p[0] = ('SELECT', p[2], 'FROM', p[4])


    def p_where_clause(self, p):
        '''
        where_clause : WHERE condition
        '''
        if len(p) == 3:
            p[0] = ('WHERE', p[2])
        else:
            p[0] = None


    def p_join_clause(self, p):
        '''
        join_clause : join_clause join_type JOIN table_reference ON condition
                    | join_type JOIN table_reference ON condition
        '''
        if len(p) == 7:
            p[0] = p[1] + [(p[2], p[4], p[6])]
        else:
            p[0] = [(p[1], p[3], p[5])]

    def p_join_type(self, p):
        '''
        join_type : INNER
                | LEFT
                | RIGHT
                | FULL
                | LEFT OUTER
                | RIGHT OUTER
                | FULL OUTER
        '''
        if len(p) == 3:
            p[0] = f'{p[1]} {p[2]}'
        else:
            p[0] = p[1]

    def p_column_list(self, p):
        '''
        column_list : column
                    | column_list COMMA column
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_column(self, p):
        '''
        column : ID
            | ID POINT ID
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = f"{p[1]}.{p[3]}"


    def p_table_reference(self, p):
        '''
        table_reference : ID
        '''
        p[0] = p[1]

    def p_condition(self, p):
        '''
        condition : expression AND expression
                | expression OR expression
                | NOT condition
                | expression EQUALS expression
                | expression EQUALS string
                | expression LESSTHAN expression
                | expression GREATERTHAN expression
                | expression COMPARISON expression
                | column COMPARISON expression
                | LPAREN condition RPAREN
                | ID EQUALS NUMBER
                | ID EQUALS ID
                | STRING EQUALS STRING
                | column COMPARISON ID
                | column EQUALS ID
                | column EQUALS column
        '''
        if len(p) == 4:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = (p[1], p[2], p[3])
        elif len(p) == 5:
            if isinstance(p[1], tuple) and len(p[1]) == 2:
                # Si p[1] es una tupla de longitud 2, es una tabla y una columna
                p[0] = ((p[1][0], p[1][1]), p[3], p[4])
            else:
                # De lo contrario, es solo una columna
                p[0] = (p[1], p[3], p[4])
        elif len(p) == 3:
            p[0] = (p[1], p[2])
        elif len(p) == 4:
            p[0] = (p[1], p[2], p[3])




    def p_insert_statement(self, p):
        '''
        insert_statement : INSERT INTO ID LPAREN column_list RPAREN VALUES LPAREN value_list RPAREN SEMICOLON
        '''
        p[0] = ('INSERT', p[2], tuple(p[5]), p[7], tuple(p[9]), p[11])

    def p_value_list(self, p):
        '''
        value_list : value
                | value_list COMMA value
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_value(self, p):
        '''
        value : NUMBER
            | string
        '''
        p[0] = p[1]

    def p_update_statement(self, p):
        '''
        update_statement : UPDATE ID SET set_clause where_clause SEMICOLON
                            | UPDATE ID SET set_clause  SEMICOLON
        '''
        p[0] = ('UPDATE', p[2], p[4], p[6])

    def p_set_clause(self, p):
        '''
        set_clause : assignment
                | set_clause COMMA assignment
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_assignment(self, p):
        '''
        assignment : ID EQUALS value
        '''
        p[0] = (p[1], '=', p[3])

    def p_delete_statement(self, p):
        '''
        delete_statement : DELETE FROM ID where_clause SEMICOLON
        '''
        p[0] = ('DELETE', p[2], 'WHERE', p[4])

    def p_drop_statement(self, p):
        '''
        drop_statement : DROP DATABASE ID SEMICOLON
                    | DROP TABLE ID SEMICOLON
                    | DROP INDEX ID SEMICOLON
        '''
        p[0] = ('DROP', p[2], p[3], p[4])

    def p_create_statement(self, p):
        '''
        create_statement : create_database_statement
                        | create_table_statement
                        | create_index_statement
        '''
        p[0] = p[1]

    def p_create_database_statement(self, p):
        '''
        create_database_statement : CREATE DATABASE ID SEMICOLON
        '''
        p[0] = ('CREATE DATABASE', p[3], p[4])

    def p_create_table_statement(self, p):
        '''
        create_table_statement : CREATE TABLE ID LPAREN column_definitions RPAREN SEMICOLON
        '''
        p[0] = ('CREATE TABLE', p[3], p[5], p[6], p[7])

    def p_column_definitions(self, p):
        '''
        column_definitions : column_definition
                        | column_definitions COMMA column_definition
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_column_definition(self, p):
        '''
        column_definition : ID data_type column_constraint_list
        '''
        p[0] = (p[1], p[2], p[3])

    def p_column_constraint_list(self, p):
        '''
        column_constraint_list : column_constraint
                            | column_constraint_list column_constraint
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_column_constraint(self, p):
        '''
        column_constraint : NOTNULL
                        | NULL
                        | AUTO_INCREMENT PRIMARYKEY
                        | PRIMARYKEY
                        | empty
        '''

        if len(p) > 1:
            p[0] = p[1]
        else:
            p[0] = ''

    def p_empty(self, p):
        'empty :'
        pass


    def p_data_type(self, p):
        '''
        data_type : INT
                | VARCHAR LPAREN NUMBER RPAREN
                | DATE
                | FLOAT
                | TEXT
                | BOOLEAN
                | TINYINT
                | SMALLINT
                | MEDIUMINT
                | INTEGER
                | BIGINT
                | REAL
                | DOUBLE
                | DECIMAL
                | NUMERIC
                | TIME
                | DATETIME
                | TINYTEXT
                | MEDIUMTEXT
                | LONGTEXT
                | TIMES
                | MINUS
                | SERIAL
        '''
        p[0] = p[1]

    def p_create_index_statement(self, p):
        '''
        create_index_statement : CREATE INDEX ID ON ID LPAREN ID RPAREN SEMICOLON
        '''
        p[0] = ('CREATE INDEX', p[3], p[5], p[7])

    def p_expression(self, p):
        '''
        expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | LPAREN expression RPAREN
                | NUMBER
                | ID
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]



    def p_string(self, p):
        '''
        string : DOUBLEQUOTE ID DOUBLEQUOTE
            | SIMPLEQUOTE ID SIMPLEQUOTE
        '''
        p[0] = p[2]

    # Manejo de errores
    def p_error(self, p):
        if p:
            self.listaErrores.append({ f"Error": f"1-Error de sintaxis: se encontró {p.lexpos}, se esperaba {p.value}"}) 
            print(f"Error de sintaxis {p.lineno}, position {p.lexpos}: Token '{p.value}'")
        else:
            self.listaErrores.append({ f"Error": f"Error de sitansis: Token indefinidos"}) 
            print("Error de sitansis: Token no definos")

    def separar_por_punto_coma(self, texto):
        parsed_queries = []

        # Eliminar saltos de línea
        texto = texto.replace('\n', '')
        
        # Dividir por punto y coma
        lineas = texto.split(';')
        
        for i, linea in enumerate(lineas):
            linea = linea.strip()
            if linea:
                if i < len(lineas) - 1:
                    parsed_query = self.parse_sql(linea+';')
                else:
                    parsed_query = self.parse_sql(linea)
                parsed_queries.append(parsed_query)
        return parsed_queries
            

    def tupla_a_objeto(self, tupla):
        objeto = {}
        objeto['consulta'] = tupla
        return objeto

    
    def sintactico(self, constulas):
        self.listaErrores = []
        results = self.separar_por_punto_coma(constulas)
        datos = []

        for err in self.listaErrores:
            datos.append(err)

        tuplas = [item for item in results if isinstance(item, tuple)]
        objetos = [self.tupla_a_objeto(tupla) for tupla in tuplas]

        for objeto in objetos:
            datos.append(objeto)
        return datos


        
        


