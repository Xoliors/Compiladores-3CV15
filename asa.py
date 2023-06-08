class SQLParser:
    def __init__(self):
        self.tokens = []
        self.current_token = None
        self.current_index = 0
        self.stack = []
        self.parse_table = {}

    def parse(self, query):
        self.tokens = self.tokenize(query)
        self.current_index = 0
        self.current_token = self.tokens[self.current_index]
        self.initialize_parse_table()
        self.stack.append('EOF')
        self.stack.append('select_statement')

        while len(self.stack) > 0:
            self.advance()  # Mover la llamada a advance() aquí
            top = self.stack[-1]

            if top in self.parse_table:
                production = self.parse_table[top]
                self.stack.pop()
                self.apply_production(production)
            elif top == self.current_token.type:
                self.stack.pop()
            else:
                self.error('Unexpected token')

        return True

    def initialize_parse_table(self):
        self.parse_table['select_statement'] = ['FROM', 'DISTINCT', 'SELECT']
        self.parse_table['field_list'] = ['FIELD', 'ASTERISK']
        self.parse_table['table_list'] = ['FIELD']
        self.parse_table['FROM'] = ['table_list']
        self.parse_table['DISTINCT'] = ['DISTINCT', 'FIELD']
        self.parse_table['SELECT'] = ['field_list']

    def apply_production(self, production):
        if isinstance(production, list):
            for symbol in reversed(production):
                self.stack.append(symbol)
        elif production == self.current_token.type:
            self.advance()
        else:
            self.error('Unexpected production')

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = Token('EOF', '')

    def tokenize(self, query):
        # Implementación del método tokenize omitida para mantener el código breve
        pass

    def error(self, message):
        raise Exception(f'Error: {message}')


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def main():
    parser = SQLParser()
    query = input("Ingrese la consulta SQL: ")
    result = parser.parse(query)
    if result:
        print("La consulta es válida.")
    else:
        print("La consulta es inválida.")


if __name__ == "__main__":
    main()
