from Token import Token
from TipoToken import TipoToken


def __str__(self):
    return f"{self.tipo} {self.lexema} "

class Scanner:
    def __init__(self, source):
        self.source = source + " "
        self.tokens = []

    def scan_tokens(self):
        estado = 0
        caracter = 0
        caracter_2 = 0
        lexema = ""
        inicio_lexema = 0

        palabras_reservadas = {
            "class": TipoToken.CLASS,
            "var": TipoToken.VAR,
            "fun": TipoToken.FUN,
            "for": TipoToken.FOR,
            "if": TipoToken.IF,
            "print": TipoToken.PRINT,
            "return": TipoToken.RETURN,
            "while": TipoToken.WHILE,
            "else": TipoToken.ELSE,
            "or": TipoToken.OR,
            "and": TipoToken.AND,
            "true": TipoToken.TRUE,
            "false": TipoToken.FALSE,
            "null": TipoToken.NULL,
            "this": TipoToken.THIS,
            "super": TipoToken.SUPER,
        }

        for i in range(len(self.source)):
            if estado == 0:
                if i < len(self.source) - 1:
                    caracter_2 = self.source[i + 1]
                caracter = self.source[i]
                if caracter == "=" and caracter_2 == "=":
                    self.tokens.append(Token(TipoToken.IGUAL_QUE, "==", i + 2))
                elif caracter == "!" and caracter_2 == "=":
                    self.tokens.append(Token(TipoToken.DIFERENTE, "!=", i + 2))
                elif caracter == ">" and caracter_2 == "=":
                    self.tokens.append(Token(TipoToken.MAYOR_IGUAL, ">=", i + 2))
                elif caracter == "<" and caracter_2 == "=":
                    self.tokens.append(Token(TipoToken.MENOR_IGUAL, "<=", i + 2))
                elif caracter == "/" and caracter_2 == "*":
                    i += 1
                    i += 1
                    caracter = self.source[i]
                    if i < len(self.source) - 1:
                        caracter_2 = self.source[i + 1]
                    while caracter != "*" and caracter_2 != "/":
                        i += 1
                        caracter = self.source[i]
                        if i < len(self.source) - 1:
                            caracter_2 = self.source[i + 1]
                    i += 1
                elif caracter == "*":
                    self.tokens.append(Token(TipoToken.ASTERISCO, "*", i + 1))
                elif caracter == ",":
                    self.tokens.append(Token(TipoToken.COMA, ",", i + 1))
                elif caracter == ".":
                    self.tokens.append(Token(TipoToken.PUNTO, ".", i + 1))
                elif caracter == ">":
                    self.tokens.append(Token(TipoToken.MAYOR, ">", i + 1))
                elif caracter == "<":
                    self.tokens.append(Token(TipoToken.MENOR, "<", i + 1))
                elif caracter == "-":
                    self.tokens.append(Token(TipoToken.GUION, "-", i + 1))
                elif caracter == "+":
                    self.tokens.append(Token(TipoToken.CRUZ, "+", i + 1))
                elif caracter == "/":
                    self.tokens.append(Token(TipoToken.DIAGONAL, "/", i + 1))
                elif caracter == "!":
                    self.tokens.append(Token(TipoToken.ADMIRACION, "!", i + 1))
                elif caracter == "=":
                    self.tokens.append(Token(TipoToken.IGUAL, "=", i + 1))
                elif caracter == "(":
                    self.tokens.append(Token(TipoToken.PARENTESIS_ABIERTO, "(", i + 1))
                elif caracter == ")":
                    self.tokens.append(Token(TipoToken.PARENTESIS_CERRADO, ")", i + 1))
                elif caracter == "{":
                    self.tokens.append(Token(TipoToken.LLAVE_ABIERTA, "{", i + 1))
                elif caracter == "}":
                    self.tokens.append(Token(TipoToken.LLAVE_CERRADA, "}", i + 1))
                elif caracter == ";":
                    self.tokens.append(Token(TipoToken.PUNTO_COMA, ";", i + 1))
                elif caracter == '"':
                    estado = 3
                    inicio_lexema = i
                elif caracter.isdigit():
                    estado = 2
                    lexema += caracter
                    inicio_lexema = i
                elif caracter.isalpha():
                    estado = 1
                    lexema += caracter
                    inicio_lexema = i

            elif estado == 1:
                if caracter.isalpha() or caracter.isdigit():
                    lexema += caracter
                else:
                    tt = palabras_reservadas.get(lexema)
                    if tt is None:
                        self.tokens.append(Token(TipoToken.IDENTIFICADOR, lexema, inicio_lexema + 1))
                    else:
                        self.tokens.append(Token(tt, lexema, inicio_lexema + 1))

                    estado = 0
                    i -= 1
                    lexema = ""
                    inicio_lexema = 0

            elif estado == 2:
                if caracter.isdigit() or caracter == ".":
                    lexema += caracter
                else:
                    tt = palabras_reservadas.get(lexema)
                    if tt is None:
                        self.tokens.append(Token(TipoToken.NUMBER, lexema, inicio_lexema + 1))
                    else:
                        self.tokens.append(Token(tt, lexema, inicio_lexema + 1))

                    estado = 0
                    i -= 1
                    lexema = ""
                    inicio_lexema = 0

            elif estado == 3:
                if caracter != '"':
                    lexema += caracter
                else:
                    tt = palabras_reservadas.get(lexema)
                    if tt is None:
                        self.tokens.append(Token(TipoToken.STRING, lexema, inicio_lexema + 1))
                    else:
                        self.tokens.append(Token(tt, lexema, inicio_lexema + 1))

                    estado = 0
                    lexema = ""
                    inicio_lexema = 0

        self.tokens.append(Token(TipoToken.EOF, "", len(self.source), 0))

        return self.tokens
