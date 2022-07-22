
from lexico import TipoToken as tt, Token, Lexico
from tabela import TabelaSimbolos
from semantico import Semantico


class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.deuErro = False

    def traduz(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.deuErro = False
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            # inicio reconhecimento do fonte
            self.tabsimb = TabelaSimbolos()
            self.semantico = Semantico()
            self.igual()
            self.consome(tt.FIMARQ)
            # fim do reconhecimento do fonte

            self.lex.fechaArquivo()
            return not self.deuErro

    def tokenEsperadoEncontrado(self, token):
        (const, msg) = token
        if self.tokenAtual.const == const:
            return True
        else:
            return False

    def consome(self, token):
        if self.tokenEsperadoEncontrado(token):
            self.tokenAtual = self.lex.getToken()
        else:
            self.deuErro = True
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
                  % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def salvaLexema(self):
        return self.tokenAtual.lexema

    def salvaLinha(self):
        return self.tokenAtual.linha

    def testaVarNaoDeclarada(self, var, linha):
        if self.deuErro:
            return
        if not self.tabsimb.existeIdent(var):
            self.deuErro = True
            msg = "Variavel " + var + " nao declarada."
            self.semantico.erroSemantico(msg, linha)
            quit()

    ##################################################################
    # Segue uma funcao para cada variavel da gramatica
    ##################################################################

    def igual(self):
        self.soma()
        self.restoigual()

    def restoigual(self):
        if self.tokenEsperadoEncontrado(tt.RESTO):
            self.consome(tt.RESTO)
            self.soma()
        else:
            pass

    def soma(self):
        self.mult()
        self.restosoma()

    def restosoma(self):
        if self.tokenEsperadoEncontrado(tt.ADD):
            self.consome(tt.ADD)
            self.soma()
        elif self.tokenEsperadoEncontrado(tt.SUB):
            self.consome(tt.SUB)
            self.soma()
        else:
            pass

    def mult(self):
        self.pot()
        self.restomult()

    def restomult(self):
        if self.tokenEsperadoEncontrado(tt.MULT):
            self.consome(tt.MULT)
            self.mult()
        elif self.tokenEsperadoEncontrado(tt.DIV):
            self.consome(tt.DIV)
            self.mult()
        else:
            pass

    def pot(self):
        self.uno()
        if self.tokenEsperadoEncontrado(tt.POT):
            self.consome(tt.POT)
            self.pot()

    def uno(self):
        if self.tokenEsperadoEncontrado(tt.ADD):
            self.consome(tt.ADD)
            self.uno()
        elif self.tokenEsperadoEncontrado(tt.SUB):
            self.consome(tt.SUB)
            self.uno()
        else:
            self.fator()

    def fator(self):
        if self.tokenEsperadoEncontrado(tt.NUM):
            self.consome(tt.NUM)
        elif self.tokenEsperadoEncontrado(tt.OPENPAR):
            self.consome(tt.OPENPAR)
            self.igual()
            self.consome(tt.CLOSEPAR)
        else:
            print('ERRO DE SINTAXE [linha %d]: fator não encontrado"'
                  % self.tokenAtual.linha)
            quit()


if __name__ == "__main__":
    nome = 'exemplo.txt'
    parser = Sintatico()
    parser.traduz(nome)
