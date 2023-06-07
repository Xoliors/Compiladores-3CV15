class SQLParser:
    def __init__(self):
        self.tokens = []
        self.current_token = None
        self.current_index = 0

    def parse(self, query):
        self.tokens = self.tokenize(query)
        self.current_index = 0
        self.current_token = self.tokens[self.current_index]
        result = self.select_statement()
        if self.current_token.type != 'EOF':
            self.error('Unexpected token')
        return result

    def tokenize(self, query):
        tokens = []
        query = query.replace(",", " , ").replace("(", " ( ").replace(")", " ) ")
        query_parts = query.split()

        for part in query_parts:
            if part.lower() == "select":
                tokens.append(Token("SELECT", "SELECT"))
            elif part.lower() == "distinct":
                tokens.append(Token("DISTINCT", "DISTINCT"))
            elif part.lower() == "from":
                tokens.append(Token("FROM", "FROM"))
            elif part == ",":
                tokens.append(Token("COMMA", ","))
            elif part == "*":
                tokens.append(Token("ASTERISK", "*"))
            elif "." in part:
                parts = part.split(".")
                for subpart in parts:
                    if not subpart.isalnum():
                        self.error(f"Invalid token: {part}")
                tokens.append(Token("FIELD", part))
            elif part.isalnum():
                tokens.append(Token("FIELD", part))
            else:
                self.error(f"Invalid token: {part}")

        tokens.append(Token('EOF', ''))
        return tokens

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = Token('EOF', '')

    def expect(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f'Expected {token_type} but got {self.current_token.type}')

    def error(self, message):
        raise Exception(f'Error: {message}')

    def select_statement(self):
        self.expect('SELECT')
        distinct = False
        if self.current_token.type == 'DISTINCT':
            self.advance()
            distinct = True
        fields = self.field_list()
        self.expect('FROM')
        tables = self.table_list()
        return {
            'distinct': distinct,
            'fields': fields,
            'tables': tables
        }

    def field_list(self):
        fields = []
        if self.current_token.type == 'ASTERISK':
            fields.append(self.current_token.value)
            self.expect('ASTERISK')
        else:
            fields.append(self.current_token.value)
            self.expect('FIELD')
            while self.current_token.type == 'COMMA':
                self.advance()
                if self.current_token.type == 'FIELD':
                    fields.append(self.current_token.value)
                    self.expect('FIELD')
                else:
                    self.error('Expected FIELD')
        return fields

    def table_list(self):
        tables = []
        tables.append(self.current_token.value)
        self.expect('FIELD')
        while self.current_token.type == 'COMMA':
            self.advance()
            if self.current_token.type == 'FIELD':
                tables.append(self.current_token.value)
                self.advance()
            else:
                self.error('Expected FIELD')
        return tables


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def main():
    parser = SQLParser()
    query = input("Ingrese la consulta SQL: ")
    result = parser.parse(query)
    print(result)


if __name__ == "__main__":
    main()
