from os import path


class TipoToken:
    RESTO = (2, '==')
    ADD = (6, '+')
    SUB = (7, '-')
    MULT = (8, '*')
    DIV = (9, '/')
    POT = (10, '^')
    OPENPAR = (11, '(')
    CLOSEPAR = (12, ')')
    NUM = (13, 'numero')
    ERROR = (14, 'erro')
    FIMARQ = (15, 'fim-de-arquivo')


class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha


class Lexico:
    # variável global responsável por guardar linha do token
    global linha

    # dicionario de palavras reservadas
    reservadas = {}

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)

            if c == '\n':
                self.linha = self.linha + 1

            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    # verifica qual é o próximo caracter
    def proxChar(self):
        c = self.getChar()
        self.ungetChar(c)
        return c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif car.isdigit():
                    estado = 2
                elif car in {'+', '-', '*', '/', '^', '(', ')'}:
                    estado = 3
                elif car == '=' and self.proxChar() == '=':
                    return Token(TipoToken.RESTO, car + self.getChar(), self.linha)
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)

            elif estado == 2:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit() and car != '.'):
                    self.ungetChar(car)
                    return Token(TipoToken.NUM, lexema, self.linha)

            elif estado == 3:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '+':
                    return Token(TipoToken.ADD, lexema, self.linha)
                if car == '-':
                    return Token(TipoToken.SUB, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.MULT, lexema, self.linha)
                elif car == '/':
                    return Token(TipoToken.DIV, lexema, self.linha)
                elif car == '^':
                    return Token(TipoToken.POT, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)


if __name__ == "__main__":

    # nome = input("Entre com o nome do arquivo: ")
    nome = 'exemplo.txt'
    lex = Lexico(nome)
    lex.abreArquivo()

    while (True):
        token = lex.getToken()
        print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
        if token.const == TipoToken.FIMARQ[0]:
            break
    lex.fechaArquivo()
