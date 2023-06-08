import sys


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.current_pos = 0

    def next_token(self):
        if self.current_pos >= len(self.input_text):
            return Token('EOF')

        char = self.input_text[self.current_pos]

        if char.isspace():
            self.current_pos += 1
            return self.next_token()

        if char.isdigit():
            return self.parse_number()

        if char.isalpha():
            return self.parse_identifier()

        if char == '{':
            self.current_pos += 1
            return Token('LBRACE', '{')

        if char == '}':
            self.current_pos += 1
            return Token('RBRACE', '}')

        if char == '(':
            self.current_pos += 1
            return Token('LPAREN', '(')

        if char == ')':
            self.current_pos += 1
            return Token('RPAREN', ')')

        if char == '+':
            self.current_pos += 1
            return Token('PLUS', '+')

        if char == '-':
            self.current_pos += 1
            return Token('MINUS', '-')

        if char == '*':
            self.current_pos += 1
            return Token('MULTIPLY', '*')

        if char == '/':
            self.current_pos += 1
            return Token('DIVIDE', '/')

        if char == '=':
            self.current_pos += 1
            return Token('EQUAL', '=')

        if char == '"':
            return self.parse_string()

        if char == ':':
            self.current_pos += 1
            return Token('COLON', ':')

        if char == ',':
            self.current_pos += 1
            return Token('COMMA', ',')

        if char == '.':
            self.current_pos += 1
            return Token('DOT', '.')

        if char == ';':
            self.current_pos += 1
            return Token('SEMICOLON', ';')

        if char == '<':
            self.current_pos += 1
            return Token('LESSTHAN', '<')

        if char == '>':
            self.current_pos += 1
            return Token('GREATERTHAN', '>')

        if char == '/':
            if self.current_pos + 1 < len(self.input_text) and self.input_text[self.current_pos + 1] == '/':
                return self.parse_single_line_comment()
            elif self.current_pos + 1 < len(self.input_text) and self.input_text[self.current_pos + 1] == '*':
                return self.parse_multiline_comment()

        raise Exception(f"Invalid character: {char}")

    def parse_number(self):
        num_str = ''
        dot_count = 0

        while self.current_pos < len(self.input_text) and (
                self.input_text[self.current_pos].isdigit() or self.input_text[self.current_pos] == '.'):
            char = self.input_text[self.current_pos]
            if char == '.':
                dot_count += 1
                if dot_count > 1:
                    break
            num_str += char
            self.current_pos += 1

        if num_str.endswith('.'):
            num_str = num_str[:-1]

        return Token('NUMBER', float(num_str))

    def parse_identifier(self):
        id_str = ''

        while self.current_pos < len(self.input_text) and (
                self.input_text[self.current_pos].isalnum() or self.input_text[self.current_pos] == '_'):
            id_str += self.input_text[self.current_pos]
            self.current_pos += 1

        if id_str == 'if':
            return Token('IF')
        elif id_str == 'else':
            return Token('ELSE')
        elif id_str == 'var':
            return Token('VAR')
        elif id_str == 'for':
            return Token('FOR')
        elif id_str == 'while':
            return Token('WHILE')
        elif id_str == 'do':
            return Token('DO')
        elif id_str == 'print':
            return Token('PRINT')
        else:
            return Token('IDENTIFIER', id_str)

    def parse_string(self):
        self.current_pos += 1
        string = ''
        while self.current_pos < len(self.input_text) and self.input_text[self.current_pos] != '"':
            string += self.input_text[self.current_pos]
            self.current_pos += 1
        self.current_pos += 1
        return Token('STRING', string)

    def parse_single_line_comment(self):
        comment = ''
        while self.current_pos < len(self.input_text) and self.input_text[self.current_pos] != '\n':
            comment += self.input_text[self.current_pos]
            self.current_pos += 1
        return Token('COMMENT', comment)

    def parse_multiline_comment(self):
        comment_start = self.current_pos
        self.current_pos += 2  # Skip the '/*'
        while self.current_pos < len(self.input_text) - 1 and self.input_text[self.current_pos:self.current_pos + 2] != '*/':
            self.current_pos += 1
        comment_end = self.current_pos
        self.current_pos += 2  # Skip the '*/'
        comment = self.input_text[comment_start:comment_end].strip()
        return Token('COMMENT', comment)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise SyntaxError(f"Invalid token: {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            expr_value = self.expr()
            self.eat('RPAREN')
            return expr_value
        elif token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return token.value
        else:
            raise SyntaxError(f"Invalid token: {token.type}")

    def term(self):
        value = self.factor()

        while self.current_token.type in ['MULTIPLY', 'DIVIDE']:
            token = self.current_token
            if token.type == 'MULTIPLY':
                self.eat('MULTIPLY')
                value *= self.factor()
            elif token.type == 'DIVIDE':
                self.eat('DIVIDE')
                denominator = self.factor()
                if denominator == 0:
                    raise ZeroDivisionError("Division by zero")
                value /= denominator

        return value

    def expr(self):
        value = self.term()

        while self.current_token.type in ['PLUS', 'MINUS']:
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                value += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                value -= self.term()

        return value

        value = self.term()

        while self.current_token.type in ['PLUS', 'MINUS']:
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                value += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                value -= self.term()

        return value


    def parse(self):
        return self.expr()


def main():
    if len(sys.argv) > 1:
        input_text = open(sys.argv[1]).read()
    else:
        input_text = input('Ingrese una cadena de texto: ')

    lexer = Lexer(input_text)
    parser = Parser(lexer)

    result = parser.parse()
    print("Resultado:", result)


if __name__ == '__main__':
    main()
