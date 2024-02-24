import re

def get_lines(code):
    lines = code.split('\n') # se divide el codigo en lineas individuales
    result = ''
    response = ''

    for line_number, line in enumerate(lines, start=1): # empieza la iteracion
        stripped_line = line.strip() # borrar espacios en blanco en los extremos
        if stripped_line: # Si NO esta en blanco
            indent = line[:len(line) - len(stripped_line)] # Calc cant de espacios
            tokens = re.findall(r'"[^"]*"|[^\s"()]+|\(\)|\.', stripped_line)
            token_string = indent # tokenes de linea actual
            for i, token in enumerate(tokens): 
                if i > 0: # en posicion mayor 0 se agrega una coma y espacio
                    token_string += ', '
                token_string += token
            array_resultante = [int(x.strip()) for x in token_string.split(',')]
            fn = maquina_dulce(array_resultante)
            response += fn[0]
            #result += token_string + fn[0] + '\n'
            result +=  fn[0] + '\n'
        else:
            result += '\n'
    return result, response


def maquina_dulce(line):
    state = 0
    line_str = ' '.join(map(str, line))
    transitions = {
        0: {'5': 5, '10': 10, '25': 25},
        5: {'5': 10, '10': 15, '25': 30},
        10: {'5': 15, '10': 20, '25': 30},
        15: {'5': 20, '10': 25, '25': 30},
        20: {'5': 25, '10': 30, '25': 30},
        25: {'5': 30, '10': 30, '25': 30},
        30: {'5': 30, '10': 30, '25': 30},
    }

    for num in line:
        if num not in [5, 10, 25]:
            return ('Los valores no son correctos', False)
        transition = transitions[state]

        state = transition.get(str(num), state)

    if state == 30:
        return (f'{line_str} => Entregar dulce', True)
    else:
        return (f'{line_str} => No entregar dulce', False)


""" num = [5,5,5,5,5,5]
print(maquina_dulce(num)) """

texto = '''5 5 5
10 10 10
5 10 25 5 10
5 5 5 5 5 5
10 25 10
5 10 25
25 5 10 10 5
25 5
10 5 10
10 10 5 5
10 25 5
5 10 25
5
5 5 10
10 5
25 10 5 5
10 25
5 10 25 10
5 5 10'''

#print(get_lines(texto)[0])