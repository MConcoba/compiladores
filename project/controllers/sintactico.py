from lexico import lexer, data_types

current_token_index = 0
tokens = []

def current_token():
    return tokens[current_token_index]

def next_token():
    global current_token_index
    current_token_index += 1

def expect(expected_type):
        token = current_token()
        if token[0] == expected_type:
            next_token()
            return token
        else:
            raise SyntaxError(f': se encontró {expected_type}, se esperaba {token[0]}')


def parse_create():
    expect('CREATE')
    next_token_type = current_token()[0]
    if next_token_type == 'DATABASE':
        return create_database()
    elif next_token_type == 'TABLE':
        return create_table()
    elif next_token_type == 'INDEX':
        return create_index()

def create_database():
    expect('DATABASE')
    db_name = expect('IDENTIFIER')[1]
    expect('SEMICOLON')
    return {'accion': 'create database', 'nombre': db_name}

def create_table():
    expect('TABLE')
    tbl_name = expect('IDENTIFIER')[1]
    expect('LPAREN')
    columns = parse_columns_tbl()
    expect('RPAREN')
    expect('SEMICOLON')
    return {'accion': 'create table', 'nombre': tbl_name, 'columnas': columns}

def parse_columns_tbl():
    columns = []
    columns.append(parse_column_tbl())
    while True:
        if current_token()[0] == 'COMMA':
            expect('COMMA')
            columns.append(parse_column_tbl())
        else:
            break
    return columns

def parse_column_tbl():
    col_name = expect('IDENTIFIER')[1]
    col_def = parse_column_definition()
    return {'nombre_col': col_name, 'definicion_col': col_def}

def parse_column_definition():
    data_type = parse_data_type()
    options = parse_data_type_options()
    return {'tipo_dato': data_type, 'opciones': options}

def parse_data_type():
    token = current_token()[0]
    if current_token()[0] in ('TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT'):
        expect(token)
        expect('LPAREN')
        length = expect('NUMBER')[1]
        expect('RPAREN')
        return {'tipo': token, 'tamaño': length}
    elif token in ('REAL', 'DOUBLE', 'FLOAT', 'DECIMAL', 'NUMERIC'):
        expect(token)
        expect('LPAREN')
        length = expect('NUMBER')[1]
        expect('COMMA')
        decimals = expect('NUMBER')[1]
        expect('RPAREN')
        return {'tipo': token, 'tamaño': length, 'decimales': decimals}
    elif token in ('DATE', 'TIME', 'DATETIME', 'TINYTEXT', 'TEXT', 'MEDIUMTEXT'):
        expect(token)
        return {'tipo': token}
    elif token == 'VARCHAR':
        expect(token)
        expect('LPAREN')
        length = expect('NUMBER')[1]
        expect('RPAREN')
        return {'tipo': token, 'tamaño': length}
    else:
        raise SyntaxError(f"Tipo de columna indefinido {token}")
        
def parse_data_type_options():
    token = current_token()[0]
    if token == 'NOTNULL':
        expect('NOTNULL')
        return 'NOTNULL'
    elif token == 'NULL':
        expect('NULL')
        return 'NULL'
    elif token == 'NOT':
        expect('NOT')
        return 'NOT'
    elif token == 'AUTO_INCREMENT PRIMARYKEY':
        expect('AUTO_INCREMENT PRIMARYKEY')
        return 'AUTO_INCREMENT PRIMARYKEY'
    elif token == 'PRIMARYKEY':
        expect('PRIMARYKEY')
        return 'PRIMARYKEY'
    else:
        return 'ε'  # ε (empty string)

def create_index():
    expect('INDEX')
    inx_name = expect('IDENTIFIER')[1]
    expect('ON')
    tbl_name = expect('IDENTIFIER')[1]
    expect('LPAREN')
    col_name = expect('IDENTIFIER')[1]
    ord = order()
    expect('RPAREN')
    expect('SEMICOLON')
    return {'accion': 'create index', 'nombre': inx_name, 'tabla': tbl_name, 'columna': col_name, 'orden': ord}

def order():
    token = current_token()[0]
    if token[0] == 'ASC' or token[0] == 'DESC':
        expect(token[0])
        return token[0]
    else:
        return 'ε'

def parse_select():
    expect('SELECT')
    fields = parse_list_fld()
    expect('FROM')
    tables = parse_table_references()
    where_clause = parse_where()
    group_by = parse_group()
    order_by = parse_order_by()
    return {
        'accion': 'select',
        'columnas': fields,
        'tabla': tables,
        'where': where_clause,
        'group_by': group_by,
        'order_by': order_by
    }

def parse_where():
    token = current_token()[0]
    if token == 'WHERE':
        expect('WHERE')
        condition = parse_condition()
        return condition
    else:
        return 'ε'  # ε
    
def parse_condition():
    return parse_expr()

def parse_expr():
    left_expr = parse_boolean_primary()
    while True:
        token = current_token()[0]
        if token in ('OR', '||', 'XOR', 'AND', '&&'):
            expect(token)
            right_expr = parse_boolean_primary()
            left_expr = {'operador': token, 'valor_izq': left_expr, 'valor_der': right_expr}
        else:
            break
    return left_expr

def parse_boolean_primary():
    left_expr = parse_simple_expr()
    token = current_token()[0]
    if token == 'IS':
        expect('IS')
        not_token = None
        if token == 'NOT':
            not_token = expect('NOT')
        expect('NULL')
        return {'operador': 'IS NULL', 'valor_izq': left_expr, 'valor_der': not_token is not None}
    elif token in ('EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'LESS_THAN_EQUALS', 'GREATER_THAN', 'GREATER_THAN_EQUALS'):
        operator = expect(token)
        if token == '(':
            expect('(')
            subquery = parse_select()
            expect(')')
            return {'operador': operator, 'valor_izq': left_expr, 'valor_der': subquery}
        else:
            right_expr = parse_simple_expr()
            return {'operador': operator, 'valor_izq': left_expr, 'valor_der': right_expr}
    else:
        return left_expr

def parse_simple_expr():
    token = current_token()[0]
    if token == 'IDENTIFIER':
        return {'tipo': 'identifier', 'valor': expect('IDENTIFIER')[1]}
    elif token == 'LITERAL':
        return {'tipo': 'literal', 'valor': expect('LITERAL')[1]}
    elif token == 'VARIABLE':
        return {'tipo': 'variable', 'valor': expect('VARIABLE')[1]}
    elif token == 'STRING':
        return {'tipo': 'string', 'valor': expect('STRING')[1]}
    elif token == 'NUMBER':
        return {'tipo': 'number', 'valor': expect('NUMBER')[1]}
    else:
        raise SyntaxError(f"Tipo de validacion invalido {token}")
    
def parse_group():
    token = current_token()[0]
    if token == 'GROUPBY':
        expect('GROUPBY')
        columns = parse_lista_columnas()
        return {'group_by': columns}
    else:
        return 'ε'  # ε

def parse_order_by():
    token = current_token()[0]
    if token == 'ORDERBY':
        expect('ORDERBY')
        columns = parse_lista_columnas()
        ord = order()
        return {'order_by': columns, 'order': ord}
    else:
        return 'ε'  # ε

def parse_lista_columnas():
    columns = []
    columns.append(expect('IDENTIFIER')[1])
    while True:
        token = current_token()[0]
        if token == 'COMMA':
            expect('COMMA')
            columns.append(expect('IDENTIFIER')[1])
        else:
            break
    return columns

def parse_list_fld():
    fields = []
    token = current_token()[1]
    if token == '*':
        expect('MULTIPLY')
        fields.append('all')
    else: 
        fields.append(parse_identifier_with_alias())
        while True:
            token = current_token()[0]
            if token == 'COMMA':
                expect('COMMA')
                fields.append(parse_identifier_with_alias())
            else:
                break
    return fields

def parse_identifier_with_alias():
    identifier = expect('IDENTIFIER')[1]
    if current_token()[0] == 'DOT':
        expect('DOT')  # consumir el punto
        sub_identifier = expect('IDENTIFIER')[1]
        return f"{identifier}.{sub_identifier}"
    return identifier

def parse_table_references():
    tables = []
    tables.append(parse_table_reference())
    while True:
        token = current_token()[0]
        if token == 'COMMA':
            expect('COMMA')
            tables.append(parse_table_reference())
        else:
            break
    return tables

def parse_table_reference():
    left_table = parse_table_factor()
    token = current_token()[0]
    if token in ('INNERJOIN', 'LEFTJOIN', 'RIGHTJOIN'):
        join_type = expect(token)
        right_table = parse_table_factor()
        join_spec = parse_join_specification()
        return {
            'join_type': join_type,
            'left_table': left_table,
            'right_table': right_table,
            'join_spec': join_spec
        }
    else:
        return left_table

def parse_table_factor():
    table_name = expect('IDENTIFIER')[1]
    alias = parse_alias()
    return {'tabla': table_name, 'alias': alias}

def parse_alias():
    token = current_token()[0]
    if token == 'AS':
        expect('AS')
        alias = expect('IDENTIFIER')[1]
        return alias
    elif token == 'IDENTIFIER':
        alias = expect('IDENTIFIER')[1]
        return alias
    else:
        return 'ε'  # ε

def parse_join_specification():
    expect('ON')
    condition = parse_condition()
    return condition

def parse_insert():
    expect('INSERT')
    expect('INTO')
    nombre_tbl = expect('IDENTIFIER')[1]
    expect('LPAREN')
    lista_columnas = parse_lista_columnas()
    expect('RPAREN')
    expect('VALUES')
    expect('LPAREN')
    value_list = parse_value_list()
    expect('RPAREN')
    return {
        'accion': 'INSERT INTO',
        'tabla': nombre_tbl,
        'columnas': lista_columnas,
        'valores': value_list
    }

def parse_value_list():
    values = [parse_value()]
    while True:
        token = current_token()[0]
        if token == 'COMMA':
            expect('COMMA')
            values.append(parse_value())

        else:
            break
    return values

def parse_value():
    token = current_token()[0]
    if token in ('NUMBER', 'STRING'):
        return expect(token)[1]
    else:
        raise SyntaxError(f"Tipo de dato invalido {token}")
                
def parse_update():
    expect('UPDATE')
    tbl_name = expect('IDENTIFIER')[1]
    expect('SET')
    assignment_list = parse_assignment_list()
    where_clause = parse_where()
    return {
        'accion': 'UPDATE',
        'tabla': tbl_name,
        'asignaciones': assignment_list,
        'where': where_clause
    }

def parse_assignment_list():
    assignments = [parse_assignment()]
    while True:
        token = current_token()[0]
        if token == 'COMMA':
            expect('COMMA')
            assignments.append(parse_assignment())

        else:
            break
    return assignments

def parse_assignment():
    nombre_col = expect('IDENTIFIER')[1]
    expect('EQUALS')
    expr_update = parse_expr_update()
    return {
        'columna': nombre_col,
        'valor': expr_update
    }

def parse_expr_update():
    token = current_token()[0]
    if token in ('NUMBER', 'STRING', 'IDENTIFIER'):
        return expect(token)[1]
    else:
        raise SyntaxError(f"Expresion de update invalido {token}")
    
def parser_delete():
        expect('DELETE')
        expect('FROM')
        tbl_name = expect('IDENTIFIER')[1]
        where_clause = parse_where()
        return {
            'accion': 'DELETE',
            'tabla': tbl_name,
            'where': where_clause
        }

def parse_sql_statement():
    token = current_token()
    if token[0] == 'CREATE':
        return parse_create()
    elif token[0] == 'SELECT':
        return parse_select()
    elif token[0] == 'INSERT':
        return parse_insert()
    elif token[0] == 'UPDATE':
        return parse_update()
    elif token[0] == 'DELETE':
        return parser_delete()
    
    else:
        raise SyntaxError(f"Inicio de consulta invalido {token}")
        #return {'error': True, 'message': f"Error de sintaxis: Inicio de consulta invalido {token}"}
    
def parse(tokens):
    global current_token_index
    global current_token
    current_token_index = 0
    current_token = lambda: tokens[current_token_index]
    return parse_sql_statement()




sql_code = "DELETEFROM personas WHERE id = 1;"

codes = """
CREATEDATABASE miBaseDeDatos;
CREATETABLE personas (id INT(10) PRIMARYKEY, nombre VARCHAR(255) NOTNULL, fecha DATE, edad VARCHAR(10));
CREATEINDEX miIndice ON miTabla(nombre ASC);
CREATEINDEX miIndice2 ON miTabla(fechanacimiento);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (1, "Juan", "1989-02-28",4);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (2, "Carlos", "2001-01-24",30,);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (3, "Maria", "1995-02-01",32);
INSERTINTO personas (id, nombre, fechanacimient ) VALUES (4, "Ligia", "1997-09-23",18);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (5, "Deisy", "1998-07-01",15);
INSERTINTO personas (id, nombre, fechanacimiento) VALUE  (6, "Navita", "2004-07-80",35);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (7, "Juan", "2015-08-11",45);
INSERTARTINTO personas (id, nombre, fechanacimiento) VALUES (8, "Juan", "2020-02-05",25);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (9, "Juan", "1989-03-15",28);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (10, "Juan", "1992-05-01",18);
INSERTINTO personas (id, nombre, fechanacimiento VALUES (11, "Roberto", "1995-06-22",17);
INSERT1NTO personas (id, nombre, fechanacimiento) VALUES (12, "Alfonso", "1990-09-20",25);
INSERTINTO personas id, nombre, fechanacimiento) VALUES (13, "Carolina", "1975-10-29",16);
INSERTINTO personas (id, nombre fechanacimiento) VALUES (14, "Navita", "1985-05-02",27);
INSERTINTO personas (id, nombre, fechanacimiento) VALUES (15, "Daniel", "2000-06-24",36);
SELEC u.nombre, u.edad FROM usuarios u WHERE u.edad ) 30 AND u.nombre LIKE "J%";
SELECT id, nombre, fechanacimiento FROM miTabla  WHERE nombre = "Juan" AND fecha >= "2020-01-01" GROUPBY nombre;
SELECT u.nombre, o.total FROM usuarios AS u INNERJOIN ordenes AS o ON u.id = o.usuario_id;
SELECT nombre, fecha_registro FROM usuarios ORDERBY fecha_registro DESC;
UPDATE miTabla SET nombre = "Pedro", fecha = "2021-01-01" WHERE id = 1;
DELETEFROM personas WHERE id = 1;
UPDATE productos SET precio = 19.99, stock = 50;
UPDATE cuentas SET balance = balance * 1.05 WHERE balance < 1000;
SELECT * FROM empleados a;
"""

def analized_parser(consultas):
    queries = consultas.replace('\n', '')
    queries = str(queries).split(';')
    results = []
    for i, query in enumerate(queries, 1):
        query = query.strip()
        res = {}
        if query:
            try:
                tok = lexer(f"{query};")
                parsed_query = parse(tok)
                res = {'consulta': i, 'tipo': parsed_query['accion'], 'datos': parsed_query, 'status': True}
            except SyntaxError as e:
                res = {'consulta': i, 'tipo': 'ERROR', 'datos': f"Error de sintaxis: {e}", 'status': False}
            results.append(res)
    return results



""" tokens = lexer(sql_code)
print(tokens)
parsed_query = parse(tokens)
print(parsed_query) """

#print(analized_parser(codes))
