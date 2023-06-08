class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_position = 0
        self.current_char = self.input_string[self.current_position]

    def advance(self):
        self.current_position += 1
        if self.current_position >= len(self.input_string):
            self.current_char = None
        else:
            self.current_char = self.input_string[self.current_position]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == ';':
                self.advance()
                return Token('SEMICOLON')
            elif self.current_char == '{':
                self.advance()
                return Token('LBRACE')
            elif self.current_char == '}':
                self.advance()
                return Token('RBRACE')
            elif self.current_char == '(':
                self.advance()
                return Token('LPAREN')
            elif self.current_char == ')':
                self.advance()
                return Token('RPAREN')
            elif self.current_char == '=':
                self.advance()
                return Token('EQUALS')
            elif self.current_char.isdigit():
                num = ''
                while self.current_char is not None and self.current_char.isdigit():
                    num += self.current_char
                    self.advance()
                return Token('NUMBER', int(num))
            elif self.current_char.isalpha():
                identifier = ''
                while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
                    identifier += self.current_char
                    self.advance()
                if identifier == 'var':
                    return Token('VAR')
                elif identifier == 'if':
                    return Token('IF')
                elif identifier == 'else':
                    return Token('ELSE')
                elif identifier == 'for':
                    return Token('FOR')
                elif identifier == 'return':
                    return Token('RETURN')
                elif identifier == 'fun':
                    return Token('FUN')
                elif identifier == 'class':
                    return Token('CLASS')
                elif identifier == 'print':
                    return Token('PRINT')
                else:
                    return Token('IDENTIFIER', identifier)
            elif self.current_char == '<':
                self.advance()
                return Token('LESSTHAN')
            elif self.current_char == '>':
                self.advance()
                return Token('GREATERTHAN')
            elif self.current_char == '+':
                self.advance()
                return Token('PLUS')
            elif self.current_char == '-':
                self.advance()
                return Token('MINUS')
            elif self.current_char == '*':
                self.advance()
                return Token('MULTIPLY')
            elif self.current_char == '/':
                self.advance()
                return Token('DIVIDE')
            elif self.current_char == '"':
                self.advance()
                string_literal = ''
                while self.current_char is not None and self.current_char != '"':
                    string_literal += self.current_char
                    self.advance()
                self.advance()  # Skip closing double quote
                return Token('STRING', string_literal)
            else:
                raise Exception(f"Unexpected character: {self.current_char}")

        return Token('EOF')

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Syntax error: Expected {token_type}, found {self.current_token.token_type}")

    def program(self):
        self.statement_list()

    def statement_list(self):
        self.statement()
        while self.current_token.token_type == 'SEMICOLON':
            self.eat('SEMICOLON')
            self.statement()

    def statement(self):
        if self.current_token.token_type == 'VAR':
            self.variable_declaration()
        elif self.current_token.token_type == 'IF':
            self.if_statement()
        elif self.current_token.token_type == 'FOR':
            self.for_loop()
        elif self.current_token.token_type == 'FUN':
            self.function_declaration()
        elif self.current_token.token_type == 'CLASS':
            self.class_declaration()
        elif self.current_token.token_type == 'IDENTIFIER':
            self.assignment_statement()
        else:
            raise Exception(f"Syntax error: Unexpected token {self.current_token.token_type}")

    def variable_declaration(self):
        self.eat('VAR')
        self.eat('IDENTIFIER')
        if self.current_token.token_type == 'EQUALS':
            self.eat('EQUALS')
            self.expression()

    def assignment_statement(self):
        self.eat('IDENTIFIER')
        self.eat('EQUALS')
        self.expression()

    def if_statement(self):
        self.eat('IF')
        self.expression()
        self.eat('LBRACE')
        self.statement_list()
        self.eat('RBRACE')
        if self.current_token.token_type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            self.statement_list()
            self.eat('RBRACE')

    def for_loop(self):
        self.eat('FOR')
        self.eat('LPAREN')
        self.variable_declaration()
        self.eat('SEMICOLON')
        self.expression()
        self.eat('SEMICOLON')
        self.assignment_statement()
        self.eat('RPAREN')
        self.eat('LBRACE')
        self.statement_list()
        self.eat('RBRACE')

    def function_declaration(self):
        self.eat('FUN')
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        if self.current_token.token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            while self.current_token.token_type == 'COMMA':
                self.eat('COMMA')
                self.eat('IDENTIFIER')
        self.eat('RPAREN')
        self.eat('LBRACE')
        self.statement_list()
        self.eat('RBRACE')

    def class_declaration(self):
        self.eat('CLASS')
        self.eat('IDENTIFIER')
        if self.current_token.token_type == 'LESSTHAN':
            self.eat('LESSTHAN')
            self.eat('IDENTIFIER')
            self.eat('GREATERTHAN')
        self.eat('LBRACE')
        self.statement_list()
        self.eat('RBRACE')

    def expression(self):
        self.term()
        while self.current_token.token_type in ['PLUS', 'MINUS']:
            if self.current_token.token_type == 'PLUS':
                self.eat('PLUS')
            elif self.current_token.token_type == 'MINUS':
                self.eat('MINUS')
            self.term()

    def term(self):
        self.factor()
        while self.current_token.token_type in ['MULTIPLY', 'DIVIDE']:
            if self.current_token.token_type == 'MULTIPLY':
                self.eat('MULTIPLY')
            elif self.current_token.token_type == 'DIVIDE':
                self.eat('DIVIDE')
            self.factor()

    def factor(self):
        if self.current_token.token_type == 'LPAREN':
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
        elif self.current_token.token_type == 'NUMBER':
            self.eat('NUMBER')
        elif self.current_token.token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        elif self.current_token.token_type == 'STRING':
            self.eat('STRING')
        else:
            raise Exception(f"Syntax error: Unexpected token {self.current_token.token_type}")

    def parse(self):
        self.program()


def test_parser(input_string):
    lexer = Lexer(input_string)
    parser = Parser(lexer)
    parser.parse()
    print("Input string is valid.")

# Prueba 1
test_parser('var a;\nvar b=0;')

# Prueba 2
test_parser('if(a<123){\n    print a;\n}')

# Prueba 3
test_parser('for(var i=0; ;){\n    print i;\n\n    if (i>100){\n        return;\n    }\n}')

# Prueba 4
test_parser('fun sumar(variable1, variable2){\n    return variabl1 + variable2;\n}')

# Prueba 5
test_parser('class Perro < Animal {\n    ladrar(){\n        print "Guauuu";\n    }\n\n    comer(){\n        while(tanque < 100){\n            tanque = tanque + 1;\n        }\n    }\n}\n\nfun crearPerro(){\n    perro = Perro();\n    perror.ladrar();\n}\n\ncrearPerro();')

# Prueba 6
test_parser('var nombre = "Hola mundo"\nfun presentarse(){\n    print nombre;\n}')

# Prueba 7
test_parser('/*\nCódigo para calcula la serie de Fibonacci\n*/\nvar fib = 0;\nvar lim = 10;\nvar aux = 1;\n\nfor(var init = 1; init <= lim; init = init + 1){\n    print fib;\n    aux = aux + fib;\n    fib = aux - fib;\n}')
