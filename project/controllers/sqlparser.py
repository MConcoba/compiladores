
import re

def analizadorSintactico( contenido):
    #consulta = separar_consultas_y_tokens(contenido)
    results = []
    consulta = separar_consultas_y_tokens(contenido)
    #print(consulta)
    for i, q in enumerate(consulta, start=1):
        #print(q)
        res = parse(q, i)
        results.append(res)

        #print(is_valid)
        #print(f"Es válido: {is_valid}")
        #print(f"Errores: {errores}")
    return results

def separar_consultas_y_tokens( script_sql):
    # Separar las consultas por el carácter ';'
    consultas = [consulta.strip() for consulta in script_sql.split(';') if consulta.strip()]
    
    # Función para fusionar tokens específicos
    def fusionar_tokens(tokens):
        fusionados = []
        i = 0
        while i < len(tokens):
            # Comprobar si el token actual y el siguiente son los que se deben fusionar
            if i < len(tokens) - 1:
                combined_token = f"{tokens[i]} {tokens[i+1]}"
                if combined_token in ['CREATE DATABASE', 'CREATE TABLE', 'INSERT INTO', 'DELETE FROM']:
                    #fusionados.append(combined_token)  # Unir los tokens con espacio entre ellos
                    fusionados.append(tokens[i] + tokens[i+1])  # Unir los tokens sin espacio entre ellos

                    i += 2
                    continue
            fusionados.append(tokens[i])
            i += 1
        return fusionados
    
    # Función para separar tokens
    def tokenizar(consulta):
        # Expresión regular para separar palabras, números y símbolos, excluyendo espacios
        pattern = re.compile(r"[\w']+|[.,!?;()=<>]+")
        return pattern.findall(consulta)
    
    # Crear una lista de listas de tokens para cada consulta
    resultado = []
    for consulta in consultas:
        tokens = tokenizar(consulta)
        tokens = fusionar_tokens(tokens)
        # Asegurarse de que cada lista de tokens termine con un ';'
        if tokens and tokens[-1] != ';':
            tokens.append(';')
        resultado.append(tokens)
    
    return resultado

def get_production( non_terminal, terminal):
    grammar = {
        "<S>": {
            "CREATEDATABASE": ["<SQLIns>"],
            "CREATETABLE": ["<SQLIns>"],
            "CREATEINDEX": ["<SQLIns>"],
            "SELECT": ["<SQLIns>"],
            "INSERTINTO": ["<SQLIns>"],
            "UPDATE": ["<SQLIns>"],
            "DELETEFROM": ["<SQLIns>"]
        },
        "<SQLIns>": {
            "CREATEDATABASE": ["<Instruccion_Crear>"],
            "CREATETABLE": ["<Instruccion_Crear>"],
            "CREATEINDEX": ["<Instruccion_Crear>"],
            "SELECT": ["<Instruccion_Listar>"],
            "INSERTINTO": ["<Instruccion_Insertar>"],
            "UPDATE": ["<Instruccion_Actualizar>"],
            "DELETEFROM": ["<Instruccion_Eliminar>"]
        },
        "<Instruccion_Crear>": {
            "CREATEDATABASE": ["<Crear_BD>"],
            "CREATETABLE": ["<Crear_TBL>"],
            "CREATEINDEX": ["<Crear_IDX>"]
        },
        "<Instruccion_Listar>": {
            "SELECT": ["SELECT", "<list_FLD>", "FROM", "<table_references>", "<Where>", "<Group>", "<OrderBY>"]
        },
        "<Crear_BD>": {
            "CREATEDATABASE": ["CREATEDATABASE", "<nombre_BD>", ";"]
        },
        "<Crear_TBL>": {
            "CREATETABLE": ["CREATETABLE", "<nombre_TBL>", "(", "<Columnas_TBL>", ")", ";"]
        },
        "<Crear_IDX>": {
            "CREATEINDEX": ["CREATEINDEX", "<nombre_IDX>", "ON", "<nombre_TBL>", "(", "<nombre_COL>", "<order>", ")"]
        },
        "<order>": {
            "ASC": ["ASC"],
            "DESC": ["DESC"],
            "ε": ["ε"]
        },
        "<Columnas_TBL>": {
            "cols_n": ["<Columna_TBL>", ",", "<Columnas_TBL>"],
            "cols_1": ["<Columna_TBL>"]
        },
        "<Columna_TBL>": {
            "col_tbl": ["<nombre_COL>", "<SPACE>", "<column_definition>"]
        },
        "<column_definition>": {
            "TINYINT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "SMALLINT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "MEDIUMINT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "INT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "INTEGER": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "BIGINT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "REAL": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "DOUBLE": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "FLOAT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "DECIMAL": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "NUMERIC": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "DATE": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "TIME": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "DATETIME": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "VARCHAR": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "TINYTEXT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "TEXT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "MEDIUMTEXT": ["<data_type>", "<SPACE>", "<data_type_options>"],
            "LONGTEXT": ["<data_type>", "<SPACE>", "<data_type_options>"]
        },
        
        "<data_type_options>": {
            "NOT NULL": ["NOT NULL"],
            "NULL": ["NULL"],
            "AUTO_INCREMENT PRIMARYKEY": ["AUTO_INCREMENT PRIMARYKEY"],
            "PRIMARYKEY": ["PRIMARYKEY"],
            "ε": ["ε"]
        },
        "<Where>": {
            "WHERE": ["WHERE", "<SPACE>", "<condition>"],
            "ε": ["ε"]
        },
        "<Group>": {
            "GROUPBY": ["GROUPBY", "<SPACE>", "<lista_Columnas>"],
            "ε": ["ε"]
        },
        "<OrderBY>": {
            "ORDERBY": ["ORDERBY", "<SPACE>", "<lista_Columnas>", "<SPACE>", "<order>"],
            "ε": ["ε"]
        },
        "<lista_Columnas>": {
            "cols_n": ["<nombre_COL>", ",", "<lista_Columnas>"],
            "cols_1": ["<nombre_COL>"]
        },
        "<list_FLD>": {
            "list_n": ["<nombre_FLD>", ",", "<list_FLD>"],
            "list_1": ["<nombre_FLD>"]
        },
        "<table_references>": {
            "identificador": ["<table_reference>"],
            "ε": ["ε"]
        },
        "<table_reference>": {
            "identificador": ["<table_factor>"]
        },
        "<table_factor>": {
            "identificador": ["<nombre_TBL>", "<alias>"]
        },
        "<condition>": {
            "OR": ["<expr>", "OR", "<expr>"],
            "||": ["<expr>", "||", "<expr>"],
            "XOR": ["<expr>", "XOR", "<expr>"],
            "AND": ["<expr>", "AND", "<expr>"],
            "&&": ["<expr>", "&&", "<expr>"],
            "NOT": ["NOT", "<expr>"],
            "!": ["!", "<expr>"],
            "boolean_primary": ["<boolean_primary>"],
            #"ε": ["ε"]
        },

            "<boolean_primary>": {
            "IS NULL": ["<simple_expr>", "IS NULL"],
            "IS NOT NULL": ["<simple_expr>", "IS NOT NULL"],
            "COMPARISON_OPERATOR": ["<simple_expr>", "<COMPARISON_OPERATOR>", "<simple_expr>"],
            "subquery": ["<simple_expr>", "<COMPARISON_OPERATOR>", "(", "<subquery>", ")"],
            "simple_expr": ["<simple_expr>"],
            #"ε": ["ε"]
        },
        "<simple_expr>": {
            "<literal>": ["<literal>"],
            "<identifier>": ["<identifier>"],
            "<variable>": ["<variable>"]
        },

        "<alias>": {
            "AS": ["AS", "<alias_name>"],
            "ε": ["ε"]
        },
        "<Instruccion_Insertar>": {
            "INSERTINTO": ["INSERTINTO", "<nombre_TBL>", "(", "<lista_Columnas>", ")", "VALUES", "(", "<value_list>", ")"]
        },
        "<value_list>": {
            "value_n": ["<value>", ",", "<value_list>"],
            "value_1": ["<value>"]
        },
        "<Instruccion_Actualizar>": {
            "UPDATE": ["UPDATE", "<SPACE>", "<nombre_TBL_UPD>", "<SPACE>", "SET", "<SPACE>", "<assignment_list>", "<Where>"]
        },
        "<assignment_list>": {
            "assing_n": ["<Assignment>", ",", "<assignment_list>"],
            "assing_1": ["<Assignment>"]
        },
        "<Assignment>": {
            "assig": ["<nombre_COL>", "=", "<expr_update>"]
        },
        "<expr_update>": {
            "identificador": ["<literal>", "<identifier>", "<variable>"]
        },
        "<Instruccion_Eliminar>": {
            "DELETEFROM": ["DELETEFROM", "<SPACE>", "<nombre_TBL>", "<Where>"]
        },
        "<nombre_BD>": {
            "identificador": ["<char_sequence>"]
        },
        "<nombre_TBL>": {
            "identificador": ["<char_sequence>"]
        },
        "<nombre_IDX>": {
            "identificador": ["<char_sequence>"]
        },
        "<nombre_COL>": {
            "identificador": ["<char_sequence>"]
        },
        "<nombre_FLD>": {
            "identificador": ["<char_sequence>"]
        },
        "<nombre_TBL_UPD>": {
            "identificador": ["<char_sequence>"]
        },
        "<alias_name>": {
            "identificador": ["<char_sequence>"]
        },
        "<char_sequence>": {
            "identificador": ["<char>", "<char_sequence>"],
            "ε": ["ε"]
        },
        "<expr>": {
            "<char_sequence>": ["<char_sequence>"],
            "<numeric_expr>": ["<numeric_expr>"]
        },
        "<SPACE>": {"espacio": " "},
        "<char>": {
            "a": ["a"], "b": ["b"], "c": ["c"], "d": ["d"], "e": ["e"],
            "f": ["f"], "g": ["g"], "h": ["h"], "i": ["i"], "j": ["j"],
            "k": ["k"], "l": ["l"], "m": ["m"], "n": ["n"], "o": ["o"],
            "p": ["p"], "q": ["q"], "r": ["r"], "s": ["s"], "t": ["t"],
            "u": ["u"], "v": ["v"], "w": ["w"], "x": ["x"], "y": ["y"],
            "z": ["z"], "A": ["A"], "B": ["B"], "C": ["C"], "D": ["D"],
            "E": ["E"], "F": ["F"], "G": ["G"], "H": ["H"], "I": ["I"],
            "J": ["J"], "K": ["K"], "L": ["L"], "M": ["M"], "N": ["N"],
            "O": ["O"], "P": ["P"], "Q": ["Q"], "R": ["R"], "S": ["S"],
            "T": ["T"], "U": ["U"], "V": ["V"], "W": ["W"], "X": ["X"],
            "Y": ["Y"], "Z": ["Z"], "0": ["0"], "1": ["1"], "2": ["2"],
            "3": ["3"], "4": ["4"], "5": ["5"], "6": ["6"], "7": ["7"],
            "8": ["8"], "9": ["9"], "_": ["_"]
        },
        "<literal>": {
            "<numeric_literal>": ["<DIGITS>", "<fraction_part>"],
            "<string_literal>": ["\"", "<CHAR_SEQUENCE_EXT>", "\""]
        },
        "<identifier>": {
            "<char_sequence>": ["<char_sequence>", "<char_sequence>"]
        },
        "<variable>": {
            "<char_sequence>": ["<char_sequence>", "<char_sequence>"]
        },
        "<COMPARISON_OPERATOR>": {
            "=": ["="],
            "<>": ["<>"],
            "!=": ["!="],
            "<": ["<"],
            "<=": ["<="],
            ">": [">"],
            ">=": [">="]
        },

    }

    if non_terminal in grammar and terminal in grammar[non_terminal]:
        return grammar[non_terminal][terminal]
    elif non_terminal in grammar and "ε" in grammar[non_terminal]:
        return grammar[non_terminal]["ε"]
    else:
        return None

def parse(input_tokens, queries):
    stack = ["<S>"]
    index = 0
    listaErrores = {}
    status_query = {}
    #listaErrores = {}  # Reiniciamos la lista de errores para cada llamada
    while stack:
        top = stack.pop()
        if index < len(input_tokens):
            current_token = input_tokens[index]
            
            if top == current_token or top == 'ε':
                index += 1
            
            elif is_non_terminal(top): 
                if top in ('<nombre_BD>', '<nombre_COL>', '<nombre_TBL>', '<table_references>', '<char_sequence>', '<nombre_FLD>', '<nombre_TBL_UPD>', '<variable>', '<identifier>', '<simple_expr>', '<expr_update>'):
                    id = validar_identificador(current_token)
                    if id == True:
                        pass
                        index += 1
                    else:
                        listaErrores[queries] = f"1-Error de sintaxis: se encontró {current_token}, se esperaba {top}"
                        status_query = ({'query': queries, 'token': input_tokens, 'menssage': f"1-Error de sintaxis: se encontró {current_token}, se esperaba {top}", 'status': False})
                elif top in ('<Columnas_TBL>'):
                    start_idx, end_idx = input_tokens.index("("), input_tokens.index(")")
                    cols = input_tokens[start_idx + 1:end_idx]

                    grupos = []
                    current_group = []

                    for item in cols:
                        if item == ',':
                            if current_group:
                                grupos.append(current_group)
                                current_group = []
                        else:
                            current_group.append(item)

                    if current_group:
                        grupos.append(current_group)

                    for gp in grupos:
                        new_token = 'cols_n' if len(gp) > 2 else  'cols_1'
                        prod = _production(top, new_token,  input_tokens, queries)
                        #print(prod)
                        if prod[0]: 
                            stack = prod[1]
                        else:
                            listaErrores[queries] = prod[1]
                            status_query = (prod[1])
                            break
                elif top in ('<Columna_TBL>'):
                    prod = _production(top, 'col_tbl', input_tokens, queries)
                    if prod[0]: 
                        stack = prod[1]
                    else:
                        listaErrores[queries] = prod[1]
                        status_query = (prod[1])

                        break
                elif top in ('<list_FLD>'):
                    if('FROM' in input_tokens):

                        start_idx, end_idx = input_tokens.index("SELECT"), input_tokens.index("FROM")
                        cols = input_tokens[start_idx + 1:end_idx]
                        if(len(cols) > 2 and (index != len(cols))) :
                            new_token = 'list_n'
                        elif (len(cols) > 2 and (index == len(cols))) :
                            new_token = 'list_1'
                        elif len(cols) < 2:
                            new_token = 'list_1'
                        else:
                            new_token = 'list_1'
                        prod = _production(top, new_token,  input_tokens, queries)
                        if prod[0]: 
                            stack = prod[1]
                        else:
                            listaErrores[queries] = prod[1]
                            status_query = (prod[1])

                            break
                    else:
                        print('no hay FROM')
                elif top in ('<lista_Columnas>'):
                    last_stack = stack
                    start_idx, end_idx = input_tokens.index("("), input_tokens.index(")")
                    cols = input_tokens[start_idx + 1:end_idx]
                    if(len(cols) > 2 and (index != len(cols))) :
                        new_token = 'cols_n'
                    elif (len(cols) > 2 and (index == len(cols))) :
                        new_token = 'cols_1'
                    elif len(cols) < 2:
                        new_token = 'cols_1'
                    prod = _production(top, new_token,  input_tokens, queries)
                    if prod[0]: 
                        index += len(cols)
                        if(prod[1] == []):
                            stack = last_stack
                    else:
                        listaErrores[queries] = prod[1]
                        status_query = (prod[1])

                        break
                elif top in ('<assignment_list>'):
                        if('WHERE' in input_tokens):
                            start_idx, end_idx = input_tokens.index("SET"), input_tokens.index("WHERE")
                            cols = input_tokens[start_idx + 1:end_idx]
                            
                            
                            grupos = []
                            current_group = []

                            for item in cols:
                                if item == ',':
                                    if current_group:
                                        grupos.append(current_group)
                                        current_group = []
                                else:
                                    current_group.append(item)

                            if current_group:
                                grupos.append(current_group)

                            for gp in grupos:
                                new_token = 'assing_n' if len(gp) > 2 else  'assing_1'
                                prod = _production(top, new_token,  input_tokens, queries)
                                #print(prod)
                                if prod[0]: 
                                    stack = prod[1]
                                else:
                                    listaErrores[queries] = prod[1]
                                    status_query = (prod[1])
                                    break
                        else:
                            print('noo')
                elif top in ('<Assignment>'):
                    prod = _production(top, 'assig', input_tokens, queries)
                    if prod[0]:
                        stack = prod[1]
                        #index -= 1
                    else:
                        listaErrores[queries] = prod[1]
                        status_query = (prod[1])
                        break
                elif top in ('<condition>'):
                    if('WHERE' in input_tokens):
                        prod = _production(top, 'boolean_primary', input_tokens, queries)
                        if prod[0]: 
                            if(prod[1] == []):
                                stack = last_stack
                            else:
                                stack = prod[1]
                        else:
                            listaErrores[queries] = prod[1]
                            status_query = (prod[1])

                            break
                    else:
                        print('nou')
                elif top in ('<boolean_primary>'):
                    if('WHERE' in input_tokens):
                        prod = _production(top, 'COMPARISON_OPERATOR', input_tokens, queries)
                        if prod[0]: 
                            if(prod[1] == []):
                                stack = last_stack
                            else:
                                stack = prod[1]
                        else:
                            listaErrores[queries] = prod[1]
                            status_query = (prod[1])

                            break
                    else:
                        print('nou')
                elif top in ('<value_list>'):
                    last_stack = stack
                    start_idx = len(input_tokens) - 1 - input_tokens[::-1].index("(")
                    end_idx = len(input_tokens) - 1 - input_tokens[::-1].index(")")
                    cols = input_tokens[start_idx + 1:end_idx]
                    if(len(cols) > 2 and (index != len(cols))) :
                        new_token = 'value_n'
                    elif (len(cols) > 2 and (index == len(cols))) :
                        new_token = 'value_1'
                    elif len(cols) < 2:
                        new_token = 'value_1'
                    prod = _production(top, new_token,  input_tokens, queries)
                    if prod[0]: 
                        index += len(cols)
                        if(prod[1] == []):
                            stack = last_stack
                    else:
                        listaErrores[queries] = prod[1]
                        status_query = (prod[1])
                        break                       
                elif top in ('<SPACE>'):
                    top = stack[-1]                
                elif top in ('<data_type>'):
                    index += 1
                elif top in ('<expr>'):
                    print('hres')

                else:
                    prod = _production(top, current_token, input_tokens, queries)
                    if prod[0]: 
                        stack = prod[1]
                    else:
                        listaErrores[queries] = prod[1]
                        status_query = (prod[1])
                        break
            else:
                listaErrores[queries] = f"5-Error de sintaxis: se encontró {current_token}, se esperaba {top}"
                status_query = ({'query': queries, 'token': input_tokens, 'menssage': f"1-Error de sintaxis: se encontró {current_token}, se esperaba {top}", 'status': False})
                break
        else:
            if top != "<S>":
                listaErrores[queries] = f"Error de sintaxis: entrada inesperada al final, se esperaba {top}"
                status_query = ({'query': queries, 'token': input_tokens, 'menssage': f"Error de sintaxis: entrada inesperada al final, se esperaba {top}", 'status': False})
            break
        
    #print(listaErrores)
    if not listaErrores:
        print('nou errs')
        listaErrores[queries] = f"{input_tokens} aceptada"
        status_query = ({'query': queries, 'token': input_tokens, 'menssage': f"Consulta aceptada", 'status': True})


    return status_query

def _production( top, token, tokens, query):
    stack = []
    production = get_production(top, token)
    #print(top, token, production)
    if production: 
        stack.extend(reversed(production))
        return [True, stack]

    else:
        #return [False, f"2-Error de sintaxis: se encontró {token}, se esperaba {top}"]
        return [False, {'query': query, 'token': tokens, 'menssage': f"1-Error de sintaxis: se encontró {token}, se esperaba {top}", 'status': False}]


def is_identifier( token):
    # Verificar si el token es una secuencia de caracteres válida
    return all(char.isalnum() or char == '_' for char in token)
def is_non_terminal( symbol):
    return symbol.startswith("<") and symbol.endswith(">")

def validar_identificador( identificador):
    # Expresión regular que coincide con letras, números y guiones bajos
    patron = r'^[a-zA-Z0-9_]+$'
    return re.match(patron, identificador) is not None
