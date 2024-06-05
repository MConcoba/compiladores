import re

# Lista de palabras clave y tipos de datos
keywords = [
    'ADD', 'ALL', 'ALTER', 'AND', 'ANY', 'AS', 'ASC', 'BACKUP', 'BETWEEN', 'CASE', 'CHECK', 'COLUMN', 'CONSTRAINT',
    'CREATE', 'DATABASE', 'DEFAULT', 'DELETE', 'DESC', 'DISTINCT', 'DROP', 'EXEC', 'EXISTS', 'FOREIGN', 'FROM', 'FULL',
    'GROUP', 'HAVING', 'IN', 'INDEX', 'INNER', 'INSERT', 'INTO', 'IS', 'JOIN', 'KEY', 'LEFT', 'LIKE', 'LIMIT', 'NOT', 'NOTNULL',
    'NULL', 'ON', 'OR', 'ORDER', 'OUTER', 'PRIMARY', 'PROCEDURE', 'RIGHT', 'ROWNUM', 'SELECT', 'SET', 'TABLE', 'TOP',
    'TRUNCATE', 'UNION', 'UNIQUE', 'UPDATE', 'VALUES', 'VIEW', 'WHERE', 'INNERJOIN', 'LEFTJOIN', 'RIGHTJOIN', 'ORDERBY',
    'PRIMARYKEY'
]

data_types = [
    'INT', 'VARCHAR', 'DATE', 'FLOAT', 'TEXT', 'BOOLEAN', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INTEGER', 'BIGINT',
    'REAL', 'DOUBLE', 'DECIMAL', 'NUMERIC', 'TIME', 'DATETIME', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT', 'TIMES',
    'MINUS', 'SERIAL'
]

# Crear los patrones de tokens para el lexer
token_patterns = []

# Añadir las palabras clave a los patrones de tokens
for keyword in keywords:
    token_patterns.append((keyword, r'\b' + keyword + r'\b'))

# Añadir los tipos de datos a los patrones de tokens
for data_type in data_types:
    token_patterns.append((data_type, r'\b' + data_type + r'\b'))

# Añadir otros tokens necesarios
token_patterns.extend([
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('NUMBER', r'\b\d+\b'),
    ('STRING', r'\'[^\']*\'|\"[^\"]*\"'),
    ('COMMA', r','),
    ('DOT', r'\.'),
    ('SEMICOLON', r';'),
    ('EQUALS', r'='),
    ('NOT_EQUALS', r'!='),
    ('LESS_THAN', r'<'),
    ('LESS_THAN_EQUALS', r'<='),
    ('GREATER_THAN', r'>'),
    ('GREATER_THAN_EQUALS', r'>='),
    ('AND', r'\bAND\b'),
    ('OR', r'\bOR\b'),
    ('NOT', r'\bNOT\b'),
    ('IS', r'\bIS\b'),
    ('NULL', r'\bNULL\b'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('WHITESPACE', r'\s+'),
    #('ARITHMETIC_OPERATOR', r'[+\-*/]'),

    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
])

# Función para generar tokens
def lexer(sql_code):
    tokens = []
    position = 0
    while position < len(sql_code):
        match = None
        for token_type, pattern in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(sql_code, position)
            if match:
                text = match.group(0)
                if token_type != 'WHITESPACE':  # Ignorar espacios en blanco
                    # Manejo especial para CREATEDATABASE
                    if token_type == 'IDENTIFIER' and text.upper() == 'CREATEDATABASE':
                        tokens.append(('CREATE', 'CREATE'))
                        tokens.append(('DATABASE', 'DATABASE'))
                    elif token_type == 'IDENTIFIER' and text.upper() == 'CREATETABLE':
                        tokens.append(('CREATE', 'CREATE'))
                        tokens.append(('TABLE', 'TABLE'))
                    elif token_type == 'IDENTIFIER' and text.upper() == 'CREATEINDEX':
                        tokens.append(('CREATE', 'CREATE'))
                        tokens.append(('INDEX', 'INDEX'))
                    elif token_type == 'IDENTIFIER' and text.upper() == 'INSERTINTO':
                        tokens.append(('INSERT', 'INSERT'))
                        tokens.append(('INTO', 'INTO'))
                    elif token_type == 'IDENTIFIER' and text.upper() == 'DELETEFROM':
                        tokens.append(('DELETE', 'DELETE'))
                        tokens.append(('FROM', 'FROM'))
                    else:
                        tokens.append((token_type, text))
                position = match.end(0)
                break
        if not match:
            raise SyntaxError(f'Valor invalido: {sql_code[position]}')
    return tokens


def analized_lexer(consultas):
    queries = consultas.replace('\n', '')
    queries = str(queries).split(';')
    results = []
    for i, query in enumerate(queries, 1):
        query = query.strip()
        if query:
            try:
                tok = lexer(f"{query};")
                one = []
                for t in tok:
                    l = {'token': t[0], 'valor': t[1]}
                    one.append(l)
                res = {'consulta': i, 'datos': one, 'query': f"{query};", 'status': True}
            except SyntaxError as e:
                res = {'consulta': i, 'datos': e, 'query': f"{query};", 'status': False}
            results.append(res)
    return results

# Código SQL de ejemplo
""" sql_code = "CREATEDATABASE mydb; CREATETABLE mytable (id INT); CREATEINDEX myindex ON mytable (id) [];"
tokens = analized_lexer(sql_code)
print(tokens) """
