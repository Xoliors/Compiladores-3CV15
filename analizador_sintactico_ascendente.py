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

# Clase Parser
class Parser:
    def __init__(self, input_tokens):
        self.input_tokens = input_tokens
        self.token_index = 0
        self.stack = []

    def parse(self):
        self.stack.append(0)

        while True:
            state = self.stack[-1]
            current_token = self.input_tokens[self.token_index]

            if current_token.token_type == 'EOF':
                if self.reduce(['QUERY']):
                    print('Consulta válida')
                else:
                    print('Error de sintaxis')
                break

            action = self.get_action(state, current_token.token_type)

            if action is None:
                print('Error de sintaxis')
                break

            if action[0] == 'shift':
                self.shift(action[1], current_token)
            elif action[0] == 'reduce':
                self.reduce(action[1])
            elif action[0] == 'accept':
                print('Consulta válida')
                break

    def get_action(self, state, token_type):
        if token_type in tokens:
            action = action_table[state].get(token_type)
        else:
            action = action_table[state].get('IDENTIFIER')
        return action

    def shift(self, next_state, token):
        self.stack.append(token)
        self.stack.append(next_state)
        self.token_index += 1

    def reduce(self, production):
        if production == ['QUERY']:
            return True

        rhs = grammar[production]

        for _ in rhs:
            self.stack.pop()
            self.stack.pop()

        lhs = production[0]
        state = self.stack[-1]

        goto_state = goto_table[state].get(lhs)

        if goto_state is None:
            return False

        self.stack.append(lhs)
        self.stack.append(goto_state)

        return True

# Tablas de análisis
grammar = {
    'S': ['QUERY'],
    'QUERY': ['SELECT', 'DISTINCT', 'COLUMN_LIST', 'FROM', 'TABLE_LIST'],
    'COLUMN_LIST': ['IDENTIFIER', 'COLUMN_LIST_TAIL'],
    'COLUMN_LIST_TAIL': ['COMMA', 'IDENTIFIER', 'COLUMN_LIST_TAIL'],
    'TABLE_LIST': ['IDENTIFIER', 'TABLE_LIST_TAIL'],
    'TABLE_LIST_TAIL': ['COMMA', 'IDENTIFIER', 'TABLE_LIST_TAIL'],
}

action_table = {
    0: {
        'SELECT': ('shift', 3),
        'IDENTIFIER': ('shift', 4),
    },
    1: {
        'EOF': ('accept', None),
    },
    2: {
        'FROM': ('shift', 5),
    },
    3: {
        'DISTINCT': ('shift', 6),
        'IDENTIFIER': ('reduce', ['COLUMN_LIST']),
        'COMMA': ('reduce', ['COLUMN_LIST']),
        'FROM': ('reduce', ['COLUMN_LIST']),
    },
    4: {
        'DOT': ('shift', 7),
        'COMMA': ('reduce', ['COLUMN_LIST']),
        'FROM': ('reduce', ['COLUMN_LIST']),
    },
    5: {
        'IDENTIFIER': ('shift', 8),
    },
    6: {
        'IDENTIFIER': ('shift', 9),
    },
    7: {
        'IDENTIFIER': ('shift', 10),
    },
    8: {
        'COMMA': ('shift', 11),
        'FROM': ('reduce', ['IDENTIFIER']),
    },
    9: {
        'FROM': ('reduce', ['TABLE_LIST']),
        'COMMA': ('reduce', ['TABLE_LIST']),
    },
    10: {
        'COMMA': ('reduce', ['IDENTIFIER']),
        'FROM': ('reduce', ['IDENTIFIER']),
    },
    11: {
        'IDENTIFIER': ('shift', 12),
    },
    12: {
        'COMMA': ('reduce', ['TABLE_LIST_TAIL']),
        'FROM': ('reduce', ['TABLE_LIST_TAIL']),
    },
}

goto_table = {
    0: {
        'S': 1,
    },
    3: {
        'QUERY': 2,
    },
    4: {
        'COLUMN_LIST': 13,
    },
    5: {
        'TABLE_LIST': 14,
    },
    8: {
        'IDENTIFIER': 15,
    },
    9: {
        'COLUMN_LIST_TAIL': 16,
    },
    10: {
        'IDENTIFIER': 17,
    },
    12: {
        'TABLE_LIST_TAIL': 18,
    },
}

# Ejemplo de uso
while True:
    sql = input("")

    if sql.lower() == "salir":
        break

    input_query = sql
    input_tokens = [Token(token) for token in sql.split()]
    parser = Parser(input_tokens)
    parser.parse()
