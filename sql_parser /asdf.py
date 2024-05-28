import re

def separar_consultas_y_tokens(script_sql):
    # Separar las consultas por el carácter ';'
    consultas = [consulta.strip() for consulta in script_sql.split(';') if consulta.strip()]
    
    # Función para fusionar tokens específicos
    def fusionar_tokens(tokens):
        fusionados = []
        i = 0
        while i < len(tokens):
            # Comprobar si el token actual y el siguiente son los que se deben fusionar
            if i < len(tokens) - 1 and ' '.join(tokens[i:i+2]) in ['CREATE DATABASE', 'CREATE TABLE', 'INSERT INTO', 'DELETE FROM']:
                fusionados.append(''.join(tokens[i:i+2]))  # Unir los tokens sin espacio entre ellos
                i += 2
            else:
                fusionados.append(tokens[i])
                i += 1
        return fusionados
    
    # Función para separar tokens
    def tokenizar(consulta):
        # Expresión regular para separar palabras, números y símbolos
        pattern = re.compile(r"[\w']+|[.,!?;()]+")
        return pattern.findall(consulta)
    
    # Crear una lista de diccionarios con consultas y sus tokens
    resultado = []
    for consulta in consultas:
        tokens = tokenizar(consulta)
        tokens = fusionar_tokens(tokens)
        resultado.append({
            'consulta': consulta,
            'tokens': tokens
        })
    
    return resultado

# Ejemplo de uso
script_sql = """
CREATE DATABASE mi_base_de_datos;
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    edad INT,
    puesto VARCHAR(50),
    salario DECIMAL(10, 2)
);

SELECT nombre, edad FROM empleados;
SELECT * FROM empleados WHERE edad > 30;
INSERT INTO empleados (nombre, edad, puesto) VALUES ('Juan Pérez', 28, 'Desarrollador');
UPDATE empleados SET edad = 29 WHERE nombre = 'Juan Pérez';
DELETE FROM empleados WHERE edad < 25;
"""

resultado = separar_consultas_y_tokens(script_sql)

# Imprimir el resultado
for r in resultado:
    print(f"Consulta: {r['consulta']}")
    print(f"Tokens: {r['tokens']}")
    print()
