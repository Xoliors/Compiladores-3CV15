import ply.lex as lex 
import codecs 
import os 

reservadas = ['BEGIN','END','IF','ELSE','FOR','THEN','WHILE','DO','CALL','CONST','VAR','PROCEDURE','OUT','IN']

tokens = reservadas+['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE','ODD','ASSIGN','NE','SLASH',
                     'LT','LTE','GT','GTE','LPARENT','RPARENT','COMMA','SEMMICOLOM','DOT','BACKSLASH',
                     'UPDATE','LBRACKET','RBRACKET','LBRACE','RBRACE','SQUOTE','DQUOTEMARK','BACKTICKS','NEWLINE'
                    ]

t_ignore = '\t '
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ODD = r'ODD'
t_ASSIGN = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMMICOLOM = r';'
t_DOT = r'\.'
t_UPDATE = r':='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SQUOTE = r'\''
t_DQUOTEMARK = r'\"'
t_BACKTICKS = r'\´'
t_SLASH = r'\/'
t_BACKSLASH = r'\\'
t_NEWLINE = r'\n+'

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z]'
	if t.value.upper() in reservadas:
		t.value = t.value.upper()
		#reservadas.get(t.value,'ID')
		t.type = t.value

	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
    
# def t_SPACE(t):
# 	r'\s+'
#     t.lexer.lineno += t.value.count("\n")
#     return t 


#dsfjksdlgjklsdgjsdgslxcvjlk-,.
def t_COMMENT(t):
	r'\#.*'
	pass

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_error(t):
	print("caracter ilegal '%s'" % t.value[0])
	t.lexer.skip(1)

def buscarFicheros(directorio):
	ficheros = []
	numArchivo = ''
	respuesta = False
	cont = 1

	for base, dirs, files in os.walk(directorio):
		ficheros.append(files)

	for file in files:
		print (str(cont)+". "+file)
		cont = cont+1

	while respuesta == False:
		numArchivo = input('\nNumero del test: ')
		for file in files:
			if file == files[int(numArchivo)-1]:
				respuesta = True
				break

	print ("Has escogido \"%s\" \n" %files[int(numArchivo)-1] + "sintaxis: Token, caracter, linea, posición")

	return files[int(numArchivo)-1]

directorio = './'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

analizador = lex.lex()

analizador.input(cadena)

while True:
	tok = analizador.token()
	if not tok : break
	print (tok)
