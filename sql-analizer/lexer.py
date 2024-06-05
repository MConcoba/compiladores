import ply.lex as lex

# Definición de tokens
tokens = [
    'SELECT', 'FROM', 'WHERE', 'ID', 'NUMBER', 'COMMA', 'EQUALS', 'INSERT', 'INTO', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'DATABASE', 'TABLE', 'INDEX','INT','VARCHAR', 'DATE', 'FLOAT', 'TEXT', 'BOOLEAN', 'LPAREN', 'RPAREN','SEMICOLON', 'STRING', 'VALUES', 'SET', 'ON','OR', 'AND', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INTEGER', 'BIGINT', 'REAL', 'DOUBLE', 'DECIMAL','NUMERIC', 'TIME', 'DATETIME', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT', 'PLUS','MINUS', 'TIMES', 'SIMPLEQUOTE', 'DOUBLEQUOTE', 'DIVIDE', 'NOT', 'LESSTHAN', 'GREATERTHAN', 'SERIAL', 'NOTNULL', 'NULL', 'AUTO_INCREMENT', 'PRIMARYKEY', "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "OUTER", "POINT", 'COMPARISON'
    ]


# Expresiones regulares para tokens
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


def t_CREATE(t):
    r'CREATE'
    return t

def t_DATABASE(t):
    r'DATABASE'
    return t

def t_INDEX(t):
    r'INDEX'
    return t

def t_TABLE(t):
    r'TABLE'
    return t

def t_SELECT(t):
    r'SELECT'
    return t

def t_FROM(t):
    r'FROM'
    return t

def t_WHERE(t):
    r'WHERE'
    return t

def t_INSERT(t):
    r'INSERT'
    return t

def t_INTO(t):
    r'INTO'
    return t

def t_VALUES(t):
    r'VALUES'
    return t

def t_UPDATE(t):
    r'UPDATE'
    return t

def t_SET(t):
    r'SET'
    return t

def t_DELETE(t):
    r'DELETE'
    return t

def t_DROP(t):
    r'DROP'
    return t

def t_ASC(t):
    r'ASC'
    return t

def t_DESC(t):
    r'DESC'
    return t

def t_EXISTS(t):
    r'EXISTS'
    return t

def t_NOTNULL(t):
    r'NOTNULL'
    return t

def t_NULL(t):
    r'NULL'
    return t

def t_AUTOI_NCREMENT(t):
    r'AUTO_INCREMENT'
    return t

def t_PRIMARYKEY(t):
    r'PRIMARYKEY'
    return t

def t_PRIMARY(t):
    r'PRIMARY'
    return t

def t_ORDERBY(t):
    r'ORDERBY'
    return t

def t_GROUPBY(t):
    r'GROUPBY'
    return t

def t_AND(t):
    r'AND'
    return t

def t_OR(t):
    r'OR'
    return t

def t_NOT(t):
    r'NOT'
    return t

def t_ISNULL(t):
    r'ISNULL'
    return t

def t_ISNOTNULL(t):
    r'ISNOTNULL'
    return t

def t_INT(t):
    r'INT'
    return t

def t_VARCHAR(t):
    r'VARCHAR'
    return t

def t_DECIMAL(t):
    r'DECIMAL'
    return t

def t_ON(t):
    r'ON'
    return t

def t_JOIN(t):
    r'JOIN'
    return t

def t_INNER(t):
    r'INNER'
    return t

def t_LEFT(t):
    r'LEFT'
    return t

def t_RIGHT(t):
    r'RIGHT'
    return t

def t_FULL(t):
    r'FULL'
    return t

def t_OUTER(t):
    r'OUTER'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convertir el valor a entero
    return t

def t_COMPARISON(t):
    r'==|<=|>=|<|>|!='
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Definición de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()



# Función para tokenizar una cadena de entrada
def tokenizsdfe(input_string):
    lexer.input(input_string)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

def tokenize(input_string):
    lexer.input(input_string)
    tokens = []
    line_number = 1  # Inicializamos el número de línea en 1
    current_position = 0  # Inicializamos la posición actual en 0
    for tok in lexer:
        if tok.lexpos > current_position:
            line_number += input_string[current_position:tok.lexpos].count('\n')
        # Actualizamos la posición actual con la posición del token
        current_position = tok.lexpos
        tok.lineno = line_number  # Asignamos el número de línea al token
        tokens.append(tok)
    return tokens

def lexico(constulas):
    datos = []
    tokens = tokenize(script_sql)
    for token in tokens:
        datos.append(token)


script_sql = """
DROPDATABASE IF EXISTS ejemplo3;
CREATEDATABASE ejemplo3;
CREATETABLE ejemplo_table (id SERIAL PRIMARY KEY, nombre VARCHAR(50));
INSERTINTO ejemplo_table (nombre) VALUES ('Ejemplo 1');
SELECT * FROM ejemplo_table;


"""

""" tokens = tokenize(script_sql)
for token in tokens:
    print(token) """


