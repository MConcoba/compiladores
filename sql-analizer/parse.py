from lexer import SQLLexer

lex = SQLLexer()
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        token = self.token_actual()
        if token[0] == 'CREATE':
            return self.create()
        elif token[0] == 'SELECT':
            return self.select()
        elif token[0] == 'INSERT':
            return self.insert()
        elif token[0] == 'UPDATE':
            return self.update()
        elif token[0] == 'DELETE':
            return self.delete()
        else:
            raise SyntaxError(f"Inicio de consulta invalido {token}")
        
    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None
        
    def match(self, token_type):
        if self.token_actual() and self.token_actual()[0] == token_type:
            self.pos += 1
            return True
        return False

    def expect(self, token_type):
        if self.match(token_type):
            return self.tokens[self.pos - 1]
        raise SyntaxError(f'Expected {token_type} at position {self.pos}')

    def create(self):
        self.expect('CREATE')
        siguiente = self.token_actual()[0]
        if siguiente == 'DATABASE':
            return self.create_database()
        elif siguiente == 'TABLE':
            return self.create_table()
        elif siguiente == 'INDEX':
            return self.create_index()
        
    def create_database(self):
        self.expect('DATABASE')
        db_name = self.expect('IDENTIFIER')[1]
        self.expect('SEMICOLON')
        return {'accion': 'create database', 'nombre': db_name}

    def create_table(self):
        self.expect('TABLE')
        tbl_name = self.expect('IDENTIFIER')[1]
        self.expect('LPAREN')
        columns = self.parse_columns_tbl()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return {'accion': 'create table', 'nombre': tbl_name, 'columnas': columns}

    def parse_columns_tbl(self):
        columns = []
        columns.append(self.parse_column_tbl())
        while True:
            if self.token_actual()[0] == 'COMMA':
                self.expect('COMMA')
                columns.append(self.parse_column_tbl())
            else:
                break
        return columns

    def parse_column_tbl(self):
        col_name = self.expect('IDENTIFIER')[1]
        col_def = self.parse_column_definition()
        return {'nombre_col': col_name, 'definicion_col': col_def}

    def parse_column_definition(self):
        data_type = self.parse_data_type()
        options = self.parse_data_type_options()
        return {'tipo_dato': data_type, 'opciones': options}

    def parse_data_type(self):
        token = self.token_actual()[0]
        if self.token_actual()[0] in ('TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT'):
            self.expect(token)
            self.expect('LPAREN')
            length = self.expect('NUMBER')[1]
            self.expect('RPAREN')
            return {'tipo': token, 'tamaño': length}
        elif token in ('REAL', 'DOUBLE', 'FLOAT', 'DECIMAL', 'NUMERIC'):
            self.expect(token)
            self.expect('LPAREN')
            length = self.expect('NUMBER')[1]
            self.expect('COMMA')
            decimals = self.expect('NUMBER')[1]
            self.expect('RPAREN')
            return {'tipo': token, 'tamaño': length, 'decimales': decimals}
        elif token in ('DATE', 'TIME', 'DATETIME', 'TINYTEXT', 'TEXT', 'MEDIUMTEXT'):
            self.expect(token)
            return {'tipo': token}
        elif token == 'VARCHAR':
            self.expect(token)
            self.expect('LPAREN')
            length = self.expect('NUMBER')[1]
            self.expect('RPAREN')
            return {'tipo': token, 'tamaño': length}
        else:
            raise SyntaxError(f"Tipo de columna indefinido {token}")
            
    def parse_data_type_options(self):
        token = self.token_actual()[0]
        if token == 'NOTNULL':
            self.expect('NOTNULL')
            return 'NOTNULL'
        elif token == 'NULL':
            self.expect('NULL')
            return 'NULL'
        elif token == 'NOT':
            self.expect('NOT')
            return 'NOT'
        elif token == 'AUTO_INCREMENT PRIMARYKEY':
            self.expect('AUTO_INCREMENT PRIMARYKEY')
            return 'AUTO_INCREMENT PRIMARYKEY'
        elif token == 'PRIMARYKEY':
            self.expect('PRIMARYKEY')
            return 'PRIMARYKEY'
        else:
            return 'ε'  # ε (empty string)

    def create_index(self):
        self.expect('INDEX')
        inx_name = self.expect('IDENTIFIER')[1]
        self.expect('ON')
        tbl_name = self.expect('IDENTIFIER')[1]
        self.expect('LPAREN')
        col_name = self.expect('IDENTIFIER')[1]
        ord = self.order()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return {'accion': 'create index', 'nombre': inx_name, 'tabla': tbl_name, 'columna': col_name, 'orden': ord}

    def order(self):
        token = self.token_actual()[0]
        if token[0] == 'ASC' or token[0] == 'DESC':
            self.expect(token[0])
            return token[0]
        else:
            return 'ε'

    def select(self):
        self.expect('SELECT')
        fields = self.parse_list_fld()
        self.expect('FROM')
        tables = self.parse_table_references()
        where_clause = self.parse_where()
        group_by = self.parse_group()
        order_by = self.parse_order_by()
        return {
            'accion': 'select',
            'columnas': fields,
            'tabla': tables,
            'where': where_clause,
            'group_by': group_by,
            'order_by': order_by
        }

    def parse_where(self):
        token = self.token_actual()[0]
        if token == 'WHERE':
            self.expect('WHERE')
            condition = self.parse_condition()
            return condition
        else:
            return 'ε'  # ε
        
    def parse_condition(self):
        return self.parse_expr()

    def parse_expr(self):
        left_expr = self.parse_boolean_primary()
        while True:
            token = self.token_actual()[0]
            if token in ('OR', '||', 'XOR', 'AND', '&&'):
                self.expect(token)
                right_expr = self.parse_boolean_primary()
                left_expr = {'operador': token, 'valor_izq': left_expr, 'valor_der': right_expr}
            else:
                break
        return left_expr

    def parse_boolean_primary(self):
        left_expr = self.parse_simple_expr()
        token = self.token_actual()[0]
        if token == 'IS':
            self.expect('IS')
            not_token = None
            if token == 'NOT':
                not_token = self.expect('NOT')
            self.expect('NULL')
            return {'operador': 'IS NULL', 'valor_izq': left_expr, 'valor_der': not_token is not None}
        elif token in ('EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'LESS_THAN_EQUALS', 'GREATER_THAN', 'GREATER_THAN_EQUALS'):
            operator = self.expect(token)
            if token == '(':
                self.expect('(')
                subquery = self.select()
                self.expect(')')
                return {'operador': operator, 'valor_izq': left_expr, 'valor_der': subquery}
            else:
                right_expr = self.parse_simple_expr()
                return {'operador': operator, 'valor_izq': left_expr, 'valor_der': right_expr}
        else:
            return left_expr

    def parse_simple_expr(self):
        token = self.token_actual()[0]
        if token == 'IDENTIFIER':
            return {'tipo': 'identifier', 'valor': self.expect('IDENTIFIER')[1]}
        elif token == 'LITERAL':
            return {'tipo': 'literal', 'valor': self.expect('LITERAL')[1]}
        elif token == 'VARIABLE':
            return {'tipo': 'variable', 'valor': self.expect('VARIABLE')[1]}
        elif token == 'STRING':
            return {'tipo': 'string', 'valor': self.expect('STRING')[1]}
        elif token == 'NUMBER':
            return {'tipo': 'number', 'valor': self.expect('NUMBER')[1]}
        else:
            raise SyntaxError(f"Tipo de validacion invalido {token}")
        
    def parse_group(self):
        token = self.token_actual()[0]
        if token == 'GROUPBY':
            self.expect('GROUPBY')
            columns = self.parse_lista_columnas()
            return {'group_by': columns}
        else:
            return 'ε'  # ε

    def parse_order_by(self):
        token = self.token_actual()[0]
        if token == 'ORDERBY':
            self.expect('ORDERBY')
            columns = self.parse_lista_columnas()
            ord = self.order()
            return {'order_by': columns, 'order': ord}
        else:
            return 'ε'  # ε

    def parse_lista_columnas(self):
        columns = []
        columns.append(self.expect('IDENTIFIER')[1])
        while True:
            token = self.token_actual()[0]
            if token == 'COMMA':
                self.expect('COMMA')
                columns.append(self.expect('IDENTIFIER')[1])
            else:
                break
        return columns

    def parse_list_fld(self):
        fields = []
        token = self.token_actual()[1]
        if token == '*':
            self.expect('MULTIPLY')
            fields.append('all')
        else: 
            fields.append(self.parse_identifier_with_alias())
            while True:
                token = self.token_actual()[0]
                if token == 'COMMA':
                    self.expect('COMMA')
                    fields.append(self.parse_identifier_with_alias())
                else:
                    break
        return fields

    def parse_identifier_with_alias(self):
        identifier = self.expect('IDENTIFIER')[1]
        if self.token_actual()[0] == 'DOT':
            self.expect('DOT')  # consumir el punto
            sub_identifier = self.expect('IDENTIFIER')[1]
            return f"{identifier}.{sub_identifier}"
        return identifier

    def parse_table_references(self):
        tables = []
        tables.append(self.parse_table_reference())
        while True:
            token = self.token_actual()[0]
            if token == 'COMMA':
                self.expect('COMMA')
                tables.append(self.parse_table_reference())
            else:
                break
        return tables

    def parse_table_reference(self):
        left_table = self.parse_table_factor()
        token = self.token_actual()[0]
        if token in ('INNERJOIN', 'LEFTJOIN', 'RIGHTJOIN'):
            join_type = self.expect(token)
            right_table = self.parse_table_factor()
            join_spec = self.parse_join_specification()
            return {
                'join_type': join_type,
                'left_table': left_table,
                'right_table': right_table,
                'join_spec': join_spec
            }
        else:
            return left_table

    def parse_table_factor(self):
        table_name = self.expect('IDENTIFIER')[1]
        alias = self.parse_alias()
        return {'tabla': table_name, 'alias': alias}

    def parse_alias(self):
        token = self.token_actual()[0]
        if token == 'AS':
            self.expect('AS')
            alias = self.expect('IDENTIFIER')[1]
            return alias
        elif token == 'IDENTIFIER':
            alias = self.expect('IDENTIFIER')[1]
            return alias
        else:
            return 'ε'  # ε

    def parse_join_specification(self):
        self.expect('ON')
        condition = self.parse_condition()
        return condition

    def insert(self):
        self.expect('INSERT')
        self.expect('INTO')
        nombre_tbl = self.expect('IDENTIFIER')[1]
        self.expect('LPAREN')
        lista_columnas = self.parse_lista_columnas()
        self.expect('RPAREN')
        self.expect('VALUES')
        self.expect('LPAREN')
        value_list = self.parse_value_list()
        self.expect('RPAREN')
        return {
            'accion': 'INSERT INTO',
            'tabla': nombre_tbl,
            'columnas': lista_columnas,
            'valores': value_list
        }

    def parse_value_list(self):
        values = [self.parse_value()]
        while True:
            token = self.token_actual()[0]
            if token == 'COMMA':
                self.expect('COMMA')
                values.append(self.parse_value())

            else:
                break
        return values

    def parse_value(self):
        token = self.token_actual()[0]
        if token in ('NUMBER', 'STRING'):
            return self.expect(token)[1]
        else:
            raise SyntaxError(f"Tipo de dato invalido {token}")
                    
    def update(self):
        self.expect('UPDATE')
        tbl_name = self.expect('IDENTIFIER')[1]
        self.expect('SET')
        assignment_list = self.parse_assignment_list()
        where_clause = self.parse_where()
        return {
            'accion': 'UPDATE',
            'tabla': tbl_name,
            'asignaciones': assignment_list,
            'where': where_clause
        }

    def parse_assignment_list(self):
        assignments = [self.parse_assignment()]
        while True:
            token = self.token_actual()[0]
            if token == 'COMMA':
                self.expect('COMMA')
                assignments.append(self.parse_assignment())

            else:
                break
        return assignments

    def parse_assignment(self):
        nombre_col = self.expect('IDENTIFIER')[1]
        self.expect('EQUALS')
        expr_update = self.parse_expr_update()
        return {
            'columna': nombre_col,
            'valor': expr_update
        }

    def parse_expr_update(self):
        token = self.token_actual()[0]
        if token in ('NUMBER', 'STRING', 'IDENTIFIER'):
            return self.expect(token)[1]
        else:
            raise SyntaxError(f"Expresion de update invalido {token}")
        
    def delete(self):
            self.expect('DELETE')
            self.expect('FROM')
            tbl_name = self.expect('IDENTIFIER')[1]
            where_clause = self.parse_where()
            return {
                'accion': 'DELETE',
                'tabla': tbl_name,
                'where': where_clause
            }
    
    
sql_code = "DELETEFROM personas WHERE id = 1;"

codes = """
CREATEDATABASE miBaseDeDatos;
"""

""" tokens = lex.lexer(sql_code) """
#print(tokens)
""" p = Parser(tokens)
parsed_query = p.parse()
print(parsed_query)  """


def analized_parser(consultas):
        queries = consultas.replace('\n', '')
        queries = str(queries).split(';')
        results = []
        for i, query in enumerate(queries, 1):
            query = query.strip()
            res = {}
            if query:
                try:
                    tok = lex.lexer(f"{query};")
                    p = Parser(tok)
                    #parsed_query = self.parse(tok)
                    parsed_query = p.parse()
                    res = {'no': i, 'consulta': f"{query};", 'respuesta': parsed_query, 'tipo': 'Consulta'}
                except SyntaxError as e:
                    res = {'no': i, 'consulta': f"{query};", 'respuesta': f"Error de sintaxis: {e}", 'tipo': 'Error'}
                results.append(res)
        return results
