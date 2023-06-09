from TipoToken import TipoToken


class Token:
    def __init__(self, tipo, lexema, linea=None, columna=None, posicion=None):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.posicion = posicion


    def __eq__(self, other):
        if not isinstance(other, Token):
            return False

        if self.tipo == other.tipo:
            return True

        return False

    def __str__(self):
        return f"Token({self.tipo}, {self.lexema}, {self.linea})"
