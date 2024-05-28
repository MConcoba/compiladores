import re

class SQLParser:
    def separar_consultas_y_tokens(self, script_sql):
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
                        print('fn')
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

# Ejemplo de uso:
parser = SQLParser()
script_sql = """
CREATE DATABASE mydatabase;
CREATE TABLE mytable (id INT, name VARCHAR(100));
INSERT INTO mytable (id, name) VALUES (1, 'John Doe');
DELETE FROM mytable WHERE id = 1;
UPDATE empleados SET edad = 29 WHERE nombre = 'Juan';
"""
tokens = parser.separar_consultas_y_tokens(script_sql)
for t in tokens:
    print(t)
