from enum import Enum

class TipoToken(Enum):
    IDENTIFICADOR = 'IDENTIFICADOR'

    # Palabras reservadas
    CLASS = 'CLASS'
    VAR = 'VAR'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    WHILE = 'WHILE'
    ELSE = 'ELSE'
    OR = 'OR'
    AND = 'AND'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NULL = 'NULL'
    THIS = 'THIS'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    SUPER = 'SUPER'

    # Caracteres
    DIFERENTE = 'DIFERENTE'
    IGUAL_QUE = 'IGUAL_QUE'
    MAYOR = 'MAYOR'
    MAYOR_IGUAL = 'MAYOR_IGUAL'
    MENOR = 'MENOR'
    MENOR_IGUAL = 'MENOR_IGUAL'
    GUION = 'GUION'
    CRUZ = 'CRUZ'
    DIAGONAL = 'DIAGONAL'
    ASTERISCO = 'ASTERISCO'
    ADMIRACION = 'ADMIRACION'
    IGUAL = 'IGUAL'
    COMA = 'COMA'
    PUNTO = 'PUNTO'
    PARENTESIS_ABIERTO = 'PARENTESIS_ABIERTO'
    PARENTESIS_CERRADO = 'PARENTESIS_CERRADO'
    LLAVE_ABIERTA = 'LLAVE_ABIERTA'
    LLAVE_CERRADA = 'LLAVE_CERRADA'
    PUNTO_COMA = 'PUNTO_COMA'

    # Final de cadena
    EOF = 'EOF'

    def __str__(self):
        return self.value
