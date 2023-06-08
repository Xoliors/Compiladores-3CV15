import sys

# Definición de tokens
tokens = [
    'SELECT', 'DISTINCT', 'FROM', 'COMMA', 'IDENTIFIER', 'DOT', 'EOF'
]

# Clase Token
class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

# Función para analizar la entrada
def parse_input(input_string):
    # Dividir la cadena de entrada en tokens
    input_tokens = tokenize(input_string)

    # Inicializar el índice del token actual
    current_token = None
    token_index = 0

    # Función para obtener el siguiente token
    def get_next_token():
        nonlocal current_token, token_index
        if token_index < len(input_tokens):
            current_token = input_tokens[token_index]
            token_index += 1
        else:
            current_token = Token('EOF')

    # Funciones de análisis sintáctico descendente
    def parse_select():
        get_next_token()
        if current_token.token_type == 'DISTINCT':
            get_next_token()
        parse_identifier_list()

    def parse_from():
        get_next_token()
        parse_table_list()

    def parse_identifier_list():
        parse_identifier()
        while current_token.token_type == 'COMMA':
            get_next_token()
            parse_identifier()

    def parse_table_list():
        parse_identifier()
        while current_token.token_type == 'COMMA':
            get_next_token()
            parse_identifier()

    def parse_identifier():
        if current_token.token_type == 'IDENTIFIER':
            get_next_token()
            if current_token.token_type == 'DOT':
                get_next_token()
                if current_token.token_type == 'IDENTIFIER':
                    get_next_token()
        else:
            raise SyntaxError('Error de sintaxis: se esperaba un identificador')

    # Función de análisis principal
    def parse():
        parse_select()
        if current_token.token_type != 'FROM':
            raise SyntaxError('Error de sintaxis: se esperaba la cláusula FROM')
        parse_from()
        if current_token.token_type != 'EOF':
            raise SyntaxError('Error de sintaxis: tokens adicionales después de la consulta')

    # Inicio del análisis
    get_next_token()
    parse()

# Función para dividir la cadena de entrada en tokens
def tokenize(input_string):
    input_tokens = []
    current_token = ""
    for char in input_string:
        if char.isspace():
            if current_token:
                input_tokens.append(Token(get_token_type(current_token), current_token))
                current_token = ""
        elif char == ',':
            if current_token:
                input_tokens.append(Token(get_token_type(current_token), current_token))
                current_token = ""
            input_tokens.append(Token('COMMA'))
        elif char == '.':
            if current_token:
                input_tokens.append(Token(get_token_type(current_token), current_token))
                current_token = ""
            input_tokens.append(Token('DOT'))
        else:
            current_token += char
    if current_token:
        input_tokens.append(Token(get_token_type(current_token), current_token))
    return input_tokens

# Función para obtener el tipo de token
def get_token_type(token_value):
    if token_value.upper() == 'SELECT':
        return 'SELECT'
    elif token_value.upper() == 'DISTINCT':
        return 'DISTINCT'
    elif token_value.upper() == 'FROM':
        return 'FROM'
    else:
        return 'IDENTIFIER'

# Ejemplo de uso
while True:
    sql = input("")

    if sql.lower() == "salir":
        break

    input_query = sql
    parse_input(input_query)
    print('Consulta válida')
