import ply.yacc as yacc
import lexer 

tokens = lexer.tokens


# Definición de la gramática
def p_statement(p):
    '''
    statement : select_statement
              | create_statement
              | insert_statement
              | update_statement
              | delete_statement
              | drop_statement
    '''
    p[0] = p[1]


def p_select_statement(p):
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


def p_where_clause(p):
    '''
    where_clause : WHERE condition
    '''
    if len(p) == 3:
        p[0] = ('WHERE', p[2])
    else:
        p[0] = None


def p_join_clause(p):
    '''
    join_clause : join_clause join_type JOIN table_reference ON condition
                | join_type JOIN table_reference ON condition
    '''
    if len(p) == 7:
        p[0] = p[1] + [(p[2], p[4], p[6])]
    else:
        p[0] = [(p[1], p[3], p[5])]

def p_join_type(p):
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

def p_column_list(p):
    '''
    column_list : column
                | column_list COMMA column
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_column(p):
    '''
    column : ID
           | ID POINT ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}.{p[3]}"


def p_table_reference(p):
    '''
    table_reference : ID
    '''
    p[0] = p[1]

def p_condition(p):
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




def p_insert_statement(p):
    '''
    insert_statement : INSERT INTO ID LPAREN column_list RPAREN VALUES LPAREN value_list RPAREN SEMICOLON
    '''
    p[0] = ('INSERT', p[2], tuple(p[5]), p[7], tuple(p[9]), p[11])

def p_value_list(p):
    '''
    value_list : value
               | value_list COMMA value
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_value(p):
    '''
    value : NUMBER
          | string
    '''
    p[0] = p[1]

def p_update_statement(p):
    '''
    update_statement : UPDATE ID SET set_clause where_clause SEMICOLON
                        | UPDATE ID SET set_clause  SEMICOLON
    '''
    p[0] = ('UPDATE', p[2], p[4], p[6])

def p_set_clause(p):
    '''
    set_clause : assignment
               | set_clause COMMA assignment
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_assignment(p):
    '''
    assignment : ID EQUALS value
    '''
    p[0] = (p[1], '=', p[3])

def p_delete_statement(p):
    '''
    delete_statement : DELETE FROM ID where_clause SEMICOLON
    '''
    p[0] = ('DELETE', p[2], 'WHERE', p[4])

def p_drop_statement(p):
    '''
    drop_statement : DROP DATABASE ID SEMICOLON
                   | DROP TABLE ID SEMICOLON
                   | DROP INDEX ID SEMICOLON
    '''
    p[0] = ('DROP', p[2], p[3], p[4])

def p_create_statement(p):
    '''
    create_statement : create_database_statement
                     | create_table_statement
                     | create_index_statement
    '''
    p[0] = p[1]

def p_create_database_statement(p):
    '''
    create_database_statement : CREATE DATABASE ID SEMICOLON
    '''
    p[0] = ('CREATE DATABASE', p[3], p[4])

def p_create_table_statement(p):
    '''
    create_table_statement : CREATE TABLE ID LPAREN column_definitions RPAREN SEMICOLON
    '''
    p[0] = ('CREATE TABLE', p[3], p[5], p[6], p[7])

def p_column_definitions(p):
    '''
    column_definitions : column_definition
                       | column_definitions COMMA column_definition
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_column_definition(p):
    '''
    column_definition : ID data_type column_constraint_list
    '''
    p[0] = (p[1], p[2], p[3])

def p_column_constraint_list(p):
    '''
    column_constraint_list : column_constraint
                           | column_constraint_list column_constraint
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_column_constraint(p):
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

def p_empty(p):
    'empty :'
    pass


def p_data_type(p):
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

def p_create_index_statement(p):
    '''
    create_index_statement : CREATE INDEX ID ON ID LPAREN ID RPAREN SEMICOLON
    '''
    p[0] = ('CREATE INDEX', p[3], p[5], p[7])

def p_expression(p):
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



def p_string(p):
    '''
    string : DOUBLEQUOTE ID DOUBLEQUOTE
           | SIMPLEQUOTE ID SIMPLEQUOTE
    '''
    p[0] = p[2]

# Manejo de errores
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}' | Constulta {p}")
    else:
        print("Syntax error: Unexpected end of input")



parser = yacc.yacc()

def parse_sql(input_string):
    return parser.parse(input_string)

# Función para parsear todas las consultas SQL
def parse_all_queries(queries):
    parsed_queries = []
    query_lines = queries.strip().split('\n')
    current_query = ''
    for lineno, line in enumerate(query_lines, start=1):
        current_query += line.strip()
        if ';' in current_query:
            #print(current_query)
            parsed_query = parse_sql(current_query)
            
            parsed_queries.append((lineno, parsed_query))
            current_query = ''
        else:
            print('no fin')
    return parsed_queries


def sintactico(constulas):
    results = parse_all_queries(otro)
    datos = []
    for result in results:
        datos.append[result]
        
script_sql = """
DROP DATABASE  ejemplo3;
CREATE DATABASE ejemplo3;
CREATE TABLE ejemplo_table (id INT PRIMARYKEY, nombre VARCHAR(50));
INSERT INTO ejemplo_table (nombre) VALUES ('Ejemplo');
SELECT nombre FROM ejemplo_table;
"""

otro = """
CREATE DATABASE mi_base_de_datos;
CREATE TABLE empleados (id INT PRIMARYKEY, nombre VARCHAR(50), edad INT, puesto VARCHAR(50), salario DECIMAL);
SELECT nombre, edad FROM empleados;
SELECT fas FROM empleados WHERE edad > 30;
INSERT INTO empleados (nombre, edad, puesto) VALUES ('Juan', 28, 'Desarrollador');
UPDATE empleados SET edad = 29 WHERE nombre = Juan;
DELETE FROM empleados WHERE edad < 25;
SELECT employees.name, departments.name FROM employees INNER JOIN departments ON employees.department_id = departments.id;

"""

""" results = parse_all_queries(otro)
for result in results:
    print(result)
 """


