from TipoToken import TipoToken

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.hayErrores = False
        self.preanalisis = None

    def parse(self):
        self.i = 0
        self.preanalisis = self.tokens[self.i]
        self.PROGRAM()

        if not self.hayErrores and self.preanalisis != TipoToken.EOF:
            print(f"Error en la posición {self.preanalisis.posicion}. No se esperaba el token {self.preanalisis.tipo}")
        elif not self.hayErrores and self.preanalisis == TipoToken.EOF:
            print("Consulta válida")

    def PROGRAM(self):
        self.DECLARATION()

    def DECLARATION(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.CLASS:
            self.CLASS_DECL()
            self.DECLARATION()
        elif self.preanalisis == TipoToken.FUN:
            self.FUN_DECL()
            self.DECLARATION()
        elif self.preanalisis == TipoToken.VAR:
            self.VAR_DECL()
            self.DECLARATION()
        elif (
            self.preanalisis == TipoToken.FOR
            or self.preanalisis == TipoToken.IF
            or self.preanalisis == TipoToken.PRINT
            or self.preanalisis == TipoToken.RETURN
            or self.preanalisis == TipoToken.WHILE
            or self.preanalisis == TipoToken.IDENTIFICADOR
        ):
            self.STATEMENT()
            self.DECLARATION()

    def CLASS_DECL(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.CLASS:
            self.coincidir(TipoToken.CLASS)
            self.coincidir(TipoToken.IDENTIFICADOR)
            self.CLASS_INHER()
            self.coincidir(TipoToken.LLAVE_ABIERTA)
            self.FUNCTIONS()
            self.coincidir(TipoToken.LLAVE_CERRADA)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def CLASS_INHER(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.MENOR:
            self.coincidir(TipoToken.MENOR)
            self.coincidir(TipoToken.IDENTIFICADOR)

    def FUN_DECL(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.FUN:
            self.coincidir(TipoToken.FUN)
            self.FUNCTION()
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def VAR_DECL(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.VAR:
            self.coincidir(TipoToken.VAR)
            self.coincidir(TipoToken.IDENTIFICADOR)
            self.VAR_INIT()
            self.coincidir(TipoToken.PUNTO_COMA)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def VAR_INIT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.IGUAL:
            self.coincidir(TipoToken.IGUAL)
            self.EXPRESSION()

    def STATEMENT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.FOR:
            self.FOR_STMT()
        elif self.preanalisis == TipoToken.IF:
            self.IF_STMT()
        elif self.preanalisis == TipoToken.PRINT:
            self.PRINT_STMT()
        elif self.preanalisis == TipoToken.RETURN:
            self.RETURN_STMT()
        elif self.preanalisis == TipoToken.WHILE:
            self.WHILE_STMT()
        elif self.preanalisis == TipoToken.IDENTIFICADOR:
            self.ASSIGNMENT()

    def FOR_STMT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.FOR:
            self.coincidir(TipoToken.FOR)
            self.coincidir(TipoToken.PARENTESIS_ABIERTO)
            self.EXPR_STMT()
            self.EXPRESSION()
            self.coincidir(TipoToken.PUNTO_COMA)
            self.EXPR_STMT()
            self.coincidir(TipoToken.PARENTESIS_CERRADO)
            self.BLOCK()
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def IF_STMT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.IF:
            self.coincidir(TipoToken.IF)
            self.coincidir(TipoToken.PARENTESIS_ABIERTO)
            self.EXPRESSION()
            self.coincidir(TipoToken.PARENTESIS_CERRADO)
            self.BLOCK()
            self.ELSE_STMT()

    def ELSE_STMT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.ELSE:
            self.coincidir(TipoToken.ELSE)
            self.BLOCK()

    def PRINT_STMT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.PRINT:
            self.coincidir(TipoToken.PRINT)
            self.coincidir(TipoToken.PARENTESIS_ABIERTO)
            self.EXPRESSION()
            self.coincidir(TipoToken.PARENTESIS_CERRADO)
            self.coincidir(TipoToken.PUNTO_COMA)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def RETURN_STMT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.RETURN:
            self.coincidir(TipoToken.RETURN)
            self.coincidir(TipoToken.PUNTO_COMA)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def WHILE_STMT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.WHILE:
            self.coincidir(TipoToken.WHILE)
            self.coincidir(TipoToken.PARENTESIS_ABIERTO)
            self.EXPRESSION()
            self.coincidir(TipoToken.PARENTESIS_CERRADO)
            self.BLOCK()

    def BLOCK(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.LLAVE_ABIERTA:
            self.coincidir(TipoToken.LLAVE_ABIERTA)
            self.DECLARATION()
            self.coincidir(TipoToken.LLAVE_CERRADA)

    def EXPRESSION(self):
        if self.hayErrores:
            return

        self.ASSIGNMENT()

    def ASSIGNMENT(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.IDENTIFICADOR:
            self.coincidir(TipoToken.IDENTIFICADOR)
            self.coincidir(TipoToken.IGUAL)
            self.EXPRESSION()

    def EXPR_STMT(self):
        if self.hayErrores:
            return

        self.EXPRESSION()
        self.coincidir(TipoToken.PUNTO_COMA)

    def FUNCTION(self):
        if self.hayErrores:
            return

        self.coincidir(TipoToken.IDENTIFICADOR)
        self.coincidir(TipoToken.PARENTESIS_ABIERTO)
        self.PARAMS()
        self.coincidir(TipoToken.PARENTESIS_CERRADO)
        self.BLOCK()

    def FUNCTIONS(self):
        if self.hayErrores:
            return

        self.FUNCTION()
        self.FUNCTIONS()

    def PARAMS(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.IDENTIFICADOR:
            self.coincidir(TipoToken.IDENTIFICADOR)
            self.PARAMS_PRIMA()

    def PARAMS_PRIMA(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.COMA:
            self.coincidir(TipoToken.COMA)
            self.coincidir(TipoToken.IDENTIFICADOR)
            self.PARAMS_PRIMA()

    def EXPRESSION(self):
        if self.hayErrores:
            return

        self.REL_EXPRESSION()
        self.EXPRESSION_PRIMA()

    def EXPRESSION_PRIMA(self):
        if self.hayErrores:
            return

        if (
            self.preanalisis == TipoToken.MAYOR
            or self.preanalisis == TipoToken.MAYOR_IGUAL
            or self.preanalisis == TipoToken.MENOR
            or self.preanalisis == TipoToken.MENOR_IGUAL
            or self.preanalisis == TipoToken.IGUAL_IGUAL
            or self.preanalisis == TipoToken.DIFERENTE
        ):
            self.REL_OP()
            self.REL_EXPRESSION()
            self.EXPRESSION_PRIMA()

    def REL_EXPRESSION(self):
        if self.hayErrores:
            return

        self.ADD_EXPRESSION()
        self.REL_EXPRESSION_PRIMA()

    def REL_EXPRESSION_PRIMA(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.OR:
            self.coincidir(TipoToken.OR)
            self.ADD_EXPRESSION()
            self.REL_EXPRESSION_PRIMA()

    def ADD_EXPRESSION(self):
        if self.hayErrores:
            return

        self.MULT_EXPRESSION()
        self.ADD_EXPRESSION_PRIMA()

    def ADD_EXPRESSION_PRIMA(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.MAS:
            self.coincidir(TipoToken.MAS)
            self.MULT_EXPRESSION()
            self.ADD_EXPRESSION_PRIMA()
        elif self.preanalisis == TipoToken.MENOS:
            self.coincidir(TipoToken.MENOS)
            self.MULT_EXPRESSION()
            self.ADD_EXPRESSION_PRIMA()

    def MULT_EXPRESSION(self):
        if self.hayErrores:
            return

        self.UNARY_EXPRESSION()
        self.MULT_EXPRESSION_PRIMA()

    def MULT_EXPRESSION_PRIMA(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.ASTERISCO:
            self.coincidir(TipoToken.ASTERISCO)
            self.UNARY_EXPRESSION()
            self.MULT_EXPRESSION_PRIMA()
        elif self.preanalisis == TipoToken.SLASH:
            self.coincidir(TipoToken.SLASH)
            self.UNARY_EXPRESSION()
            self.MULT_EXPRESSION_PRIMA()

    def UNARY_EXPRESSION(self):
        if self.hayErrores:
            return

        if (
            self.preanalisis == TipoToken.MENOS
            or self.preanalisis == TipoToken.NOT
        ):
            self.UNARY_OP()
            self.UNARY_EXPRESSION()
        else:
            self.PRIMARY_EXPRESSION()

    def PRIMARY_EXPRESSION(self):
        if self.hayErrores:
            return

        if self.preanalisis == TipoToken.PARENTESIS_ABIERTO:
            self.coincidir(TipoToken.PARENTESIS_ABIERTO)
            self.EXPRESSION()
            self.coincidir(TipoToken.PARENTESIS_CERRADO)
        elif self.preanalisis == TipoToken.ENTERO:
            self.coincidir(TipoToken.ENTERO)
        elif self.preanalisis == TipoToken.DECIMAL:
            self.coincidir(TipoToken.DECIMAL)
        elif self.preanalisis == TipoToken.CADENA:
            self.coincidir(TipoToken.CADENA)
        elif self.preanalisis == TipoToken.TRUE:
            self.coincidir(TipoToken.TRUE)
        elif self.preanalisis == TipoToken.FALSE:
            self.coincidir(TipoToken.FALSE)
        elif self.preanalisis == TipoToken.IDENTIFICADOR:
            self.coincidir(TipoToken.IDENTIFICADOR)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def REL_OP(self):
        if self.hayErrores:
            return

        if (
            self.preanalisis == TipoToken.MAYOR
            or self.preanalisis == TipoToken.MAYOR_IGUAL
            or self.preanalisis == TipoToken.MENOR
            or self.preanalisis == TipoToken.MENOR_IGUAL
            or self.preanalisis == TipoToken.IGUAL_IGUAL
            or self.preanalisis == TipoToken.DIFERENTE
        ):
            self.coincidir(self.preanalisis.tipo)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def UNARY_OP(self):
        if self.hayErrores:
            return

        if (
            self.preanalisis == TipoToken.MENOS
            or self.preanalisis == TipoToken.NOT
        ):
            self.coincidir(self.preanalisis.tipo)
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}")

    def coincidir(self, tipoEsperado):
        if self.preanalisis.tipo == tipoEsperado:
            self.i += 1
            if self.i < len(self.tokens):
                self.preanalisis = self.tokens[self.i]
        else:
            self.hayErrores = True
            print(f"Error en la posición {self.preanalisis.posicion}. Se esperaba {tipoEsperado}")
