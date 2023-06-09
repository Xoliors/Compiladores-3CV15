import sys
from Scanner import Scanner
from Parser import Parser

def ejecutar():
    source = "tu_codigo_fuente_aqui"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

class Principal:
    existen_errores = False

    @staticmethod
    def main(args):
        Principal.ejecutar_prompt()

    @staticmethod
    def ejecutar_prompt():
        while True:
            linea = input(">>> ")
            
            if not linea:
                break  # Presionar Enter sin ingresar nada
            
            archivo = linea.strip()
            
            if archivo:
                try:
                    with open(archivo, "r") as file:
                        contenido = file.read().replace("\n", "").replace("\r", "")
                        print(contenido)
                        Principal.ejecutar(contenido)
                        Principal.existen_errores = False
                except FileNotFoundError:
                    print("El archivo no existe.")
            else:
                Principal.ejecutar(linea)
                Principal.existen_errores = False

    @staticmethod
    def ejecutar(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        parser.parse()

    @staticmethod
    def error(linea, mensaje):
        Principal.reportar(linea, "", mensaje)

    @staticmethod
    def reportar(linea, donde, mensaje):
        print(f"[linea {linea}] Error {donde}: {mensaje}", file=sys.stderr)
        Principal.existen_errores = True

if __name__ == "__main__":
    Principal.main(sys.argv[1:])
