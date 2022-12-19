import ply.lex as lex
from ply import yacc
from cProfile import label
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import filedialog as fd

#Análise Léxica
                                               # Palavras Reservadas do Compilador
reserved = {
   'IF' : 'IF',
   'ELIF' : 'ELIF',
   'ELSE' : 'ELSE',
   'WHILE' : 'WHILE',
   'MOVER' : 'MOVER',
   'MOVER_DIREITA' : 'MOVER_DIREITA',
   'MOVER_ESQUERDA' : 'MOVER_ESQUERDA',
   'MOVER_CIMA':'MOVER_CIMA',
   'MOVER_BAIXO':'MOVER_BAIXO',
   'POSICAO_COBRA':'POSICAO_COBRA',
   'POSICAO_ALIMENTO':'POSICAO_ALIMENTO',
   'IFSULDEMINAS':'IFSULDEMINAS',
   'FOR':'FOR',
   'PONTUACAO':'PONTUACAO',
   'TRUE':'TRUE',
   'FALSE':'FALSE',
   'PRINTF':'PRINTF',
   'AUX':'AUX',
   'IMP':'IMP',
}

# Lista para os nomes dos tokens. Esta parte é sempre Requerida pela Biblioteca PLY
tokens = [
                                                     #Operadores Matemáticos
'OP_MAT_MAIS' ,        #+
'OP_MAT_MENOS' ,       #-
'OP_MAT_VEZES',        #*
'OP_MAT_DIVIDE',       #/
'OP_MAT_MODULO',       #%
                                                    #Operadores de Execução
'OP_EXEC_DOIS_PONTOS' ,         #:
'OP_EXEC_PONTO_VIRGULA',        #;
'OP_EXEC_VIRGULA',              #,
'OP_EXEC_PONTO',                #.
                                                    #Operadores de Impressão
'OP_IMP_ASPAS',    #"
'OP_COMENTARIO',   ##
'OP_FINALLINHA',   #final de linha
                                                    #Operadores de Atribuição
'OP_ATRIB_NEGACAO',          #~
'OP_ATRIB_IGUAL',            #=
'OP_ATRIB_MAIS_IGUAL',       #+=
'OP_ATRIB_MENOS_IGUAL',      #-=
'OP_ATRIB_VEZES_IGUAL',      #*=
'OP_ATRIB_DIVIDE_IGUAL',     #/=
                                                     #Operadores Relacionais
'OP_REL_MENOR',           #<
'OP_REL_MAIOR',           #>
'OP_REL_MENOR_IGUAL',     #<=
'OP_REL_MAIOR_IGUAL',     #>=
'OP_REL_DUPLO_IGUAL',     #==
'OP_REL_DIFERENTE',       #!=
'OP_REL_E',               #&
'OP_REL_OU' ,             #|
                                                    #Operadores de Prioridade
'OP_PRIO_ABRE_PARENTESES',       #(
'OP_PRIO_FECHA_PARENTESES',      #)
'OP_PRIO_ABRE_COLCHETES',        #[
'OP_PRIO_FECHA_COLCHETES',       #]
'OP_PRIO_ABRE_CHAVES',           #{
'OP_PRIO_FECHA_CHAVES',          #}
                                                    #Identificadores
'INTEIRO',      #inteiro
'DOUBLE',       #double
'STRING',       #string
'CHAR',         #char
'VARIAVEL',     #variavel
'TESTE',

#para a criação dos RegEx (para verificar as compatibilidades) com o PLY,as verificações tem que ter uma "chamada" pelo token, é padrão
'IGNORE',      #Ignorar tabulação e espaço

'variavel_mf', #variavel mal formada
'numero_mf',   #numero mal formado
'string_mf',   #string mal formada

] + list(reserved.values()) #concateno com as palavras reservadas para verificação

#Regras de expressão regular (RegEx) para tokens simples
t_OP_MAT_MAIS    = r'\+'
t_OP_MAT_MENOS   = r'-'
t_OP_MAT_VEZES   = r'\*'
t_OP_MAT_DIVIDE  = r'/'
t_OP_MAT_MODULO = r'\%'

t_OP_EXEC_DOIS_PONTOS = r'\:'
t_OP_EXEC_PONTO_VIRGULA = r'\;'
t_OP_EXEC_VIRGULA = r'\,'
t_OP_EXEC_PONTO = r'\.'

t_OP_IMP_ASPAS = r'\"'
t_OP_COMENTARIO = r'\#.*'

t_IFSULDEMINAS = r'IFSULDEMINAS'
t_WHILE = r'WHILE'
t_IF = r'IF'
t_ELIF = r'ELIF'
t_ELSE = r'ELSE'
t_MOVER = r'MOVER'
t_MOVER_DIREITA = r'MOVER_DIREITA'
t_MOVER_ESQUERDA =  r'MOVER_ESQUERDA'
t_MOVER_CIMA = r'MOVER_CIMA'
t_MOVER_BAIXO = r'MOVER_BAIXO'
t_POSICAO_COBRA = r'POSICAO_COBRA'
t_POSICAO_ALIMENTO = r'POSICAO_ALIMENTO'
t_FOR = r'FOR'
t_PONTUACAO = r'PONTUACAO'
t_TRUE = r'TRUE'
t_FALSE = r'FALSE'
t_PRINTF = r'PRINTF'
t_AUX = r'AUX'
t_IMP = r'IMP'

t_OP_ATRIB_NEGACAO = r'\~'
t_OP_ATRIB_IGUAL = r'\='
t_OP_ATRIB_MAIS_IGUAL = r'\+\='
t_OP_ATRIB_MENOS_IGUAL = r'\-\='
t_OP_ATRIB_VEZES_IGUAL = r'\*\='
t_OP_ATRIB_DIVIDE_IGUAL = r'\/\='

t_OP_REL_MENOR = r'\<'
t_OP_REL_MAIOR= r'\>'
t_OP_REL_MENOR_IGUAL = r'\<\='
t_OP_REL_MAIOR_IGUAL = r'\>\='
t_OP_REL_DUPLO_IGUAL = r'\=\='
t_OP_REL_DIFERENTE = r'\!\='
t_OP_REL_E= r'\&'
t_OP_REL_OU = r'\|'

t_OP_PRIO_ABRE_PARENTESES  = r'\('
t_OP_PRIO_FECHA_PARENTESES  = r'\)'
t_OP_PRIO_ABRE_COLCHETES = r'\['
t_OP_PRIO_FECHA_COLCHETES = r'\]'
t_OP_PRIO_ABRE_CHAVES = r'\{'
t_OP_PRIO_FECHA_CHAVES = r'\}'

t_ignore  = ' \t' #ignora espaço e tabulação

#Regras de expressão regular (RegEx) para tokens mais "complexos"

def t_STRING(t):
    r'("[^"]*")'
    return t

def t_string_mf(t):
    r'("[^"]*)'
    return t

def t_variavel_mf(t):
    r'([0-9]+[a-z]+)|([@!#$%&*]+[a-z]+|[a-z]+\.[0-9]+|[a-z]+[@!#$%&*]+)'
    return t

def t_numero_mf(t):
    r'([0-9]+\.[a-z]+[0-9]+)|([0-9]+\.[a-z]+)|([0-9]+\.[0-9]+[a-z]+)'
    return t

def t_DOUBLE(t):
    r'([0-9]+\.[0-9]+)|([0-9]+\.[0-9]+)'
    return t

def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARIAVEL(t):
   r'[a-z][a-z_0-9]*'
   return t

#Defina uma regra para que seja possível rastrear o números de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_OP_FINALLINHA(t):
    r'\''
    return t
    t.lexer.lineno += len(t.value)

#Regra de tratamento de erros
erroslexicos = []
def t_error(t):
    erroslexicos.append(t)
    t.lexer.skip(1)

#Análise Sintática

def p_statements_multiple(p):
    '''
    statements : statements statement
    '''

def p_statements_single(p):
    '''
    statements : statement
    '''

def p_statement_comentarios(p):
    '''
    statement : OP_COMENTARIO
    '''

def p_statement_ifsuldeminas(p):
    '''
    statement : IFSULDEMINAS OP_FINALLINHA
    '''

def p_statement_while(p):
    '''
    statement : WHILE OP_PRIO_ABRE_PARENTESES cond_param OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
    '''

def p_statement_para(p):
    '''
    statement : FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL INTEIRO OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES

              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL reserv OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL reserv OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL reserv OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL reserv OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv OP_ATRIB_IGUAL reserv OP_EXEC_VIRGULA cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES

              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL VARIAVEL OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv cond_param OP_EXEC_VIRGULA VARIAVEL OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES VARIAVEL cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
              | FOR OP_PRIO_ABRE_PARENTESES reserv cond_param OP_EXEC_VIRGULA reserv OP_ATRIB_IGUAL reserv OP_MAT_MAIS INTEIRO  OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
    '''

def p_statement_atribuicaoValorVariavel(p):
    '''
    statement : VARIAVEL OP_ATRIB_IGUAL expr OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL STRING OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL VARIAVEL OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL reserv OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL INTEIRO OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL DOUBLE OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL CHAR OP_FINALLINHA
            | VARIAVEL OP_ATRIB_IGUAL funcao OP_FINALLINHA
            | VARIAVEL OP_ATRIB_MAIS_IGUAL INTEIRO
            | VARIAVEL OP_ATRIB_MAIS_IGUAL DOUBLE
            | VARIAVEL OP_ATRIB_MAIS_IGUAL VARIAVEL
            | VARIAVEL OP_ATRIB_MAIS_IGUAL reserv
            | VARIAVEL OP_ATRIB_MENOS_IGUAL INTEIRO
            | VARIAVEL OP_ATRIB_MENOS_IGUAL DOUBLE
            | VARIAVEL OP_ATRIB_MENOS_IGUAL VARIAVEL
            | VARIAVEL OP_ATRIB_MENOS_IGUAL reserv
            | reserv OP_ATRIB_IGUAL expr OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL STRING OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL VARIAVEL OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL reserv OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL INTEIRO OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL DOUBLE OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL CHAR OP_FINALLINHA
            | reserv OP_ATRIB_IGUAL funcao OP_FINALLINHA
            | reserv OP_ATRIB_MAIS_IGUAL INTEIRO
            | reserv OP_ATRIB_MAIS_IGUAL DOUBLE
            | reserv OP_ATRIB_MAIS_IGUAL VARIAVEL
            | reserv OP_ATRIB_MAIS_IGUAL reserv
            | reserv OP_ATRIB_MENOS_IGUAL INTEIRO
            | reserv OP_ATRIB_MENOS_IGUAL DOUBLE
            | reserv OP_ATRIB_MENOS_IGUAL VARIAVEL
            | reserv OP_ATRIB_MENOS_IGUAL reserv
    '''

def p_statement_condicionais(p):
    '''
    statement : IF OP_PRIO_ABRE_PARENTESES cond_param OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
            | IF OP_PRIO_ABRE_PARENTESES cond_param OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES senaose
            | IF OP_PRIO_ABRE_PARENTESES cond_param OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES senaose ELSE OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
            | IF OP_PRIO_ABRE_PARENTESES cond_param OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES ELSE OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
    '''

def p_statement_funcao_invocada(p):
    '''
    statement : funcao OP_FINALLINHA
    '''

def p_statement_definir_funcao(p):
    '''
    statement : funcao OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
    '''

def p_parametro_condicional(p):
    '''
    cond_param :  VARIAVEL OP_REL_MENOR INTEIRO
                | VARIAVEL OP_REL_MENOR DOUBLE
                | VARIAVEL OP_REL_MENOR VARIAVEL
                | VARIAVEL OP_REL_MENOR reserv

                | reserv OP_REL_MENOR INTEIRO
                | reserv OP_REL_MENOR DOUBLE
                | reserv OP_REL_MENOR VARIAVEL
                | reserv OP_REL_MENOR reserv

                | VARIAVEL OP_REL_MAIOR INTEIRO
                | VARIAVEL OP_REL_MAIOR DOUBLE
                | VARIAVEL OP_REL_MAIOR VARIAVEL
                | VARIAVEL OP_REL_MAIOR reserv

                | reserv OP_REL_MAIOR INTEIRO
                | reserv OP_REL_MAIOR DOUBLE
                | reserv OP_REL_MAIOR VARIAVEL
                | reserv OP_REL_MAIOR reserv

                | VARIAVEL OP_REL_MENOR_IGUAL INTEIRO
                | VARIAVEL OP_REL_MENOR_IGUAL DOUBLE
                | VARIAVEL OP_REL_MENOR_IGUAL VARIAVEL
                | VARIAVEL OP_REL_MENOR_IGUAL reserv

                | reserv OP_REL_MENOR_IGUAL INTEIRO
                | reserv OP_REL_MENOR_IGUAL DOUBLE
                | reserv OP_REL_MENOR_IGUAL VARIAVEL
                | reserv OP_REL_MENOR_IGUAL reserv

                | VARIAVEL OP_REL_MAIOR_IGUAL INTEIRO
                | VARIAVEL OP_REL_MAIOR_IGUAL DOUBLE
                | VARIAVEL OP_REL_MAIOR_IGUAL VARIAVEL
                | VARIAVEL OP_REL_MAIOR_IGUAL reserv

                | reserv OP_REL_MAIOR_IGUAL INTEIRO
                | reserv OP_REL_MAIOR_IGUAL DOUBLE
                | reserv OP_REL_MAIOR_IGUAL VARIAVEL
                | reserv OP_REL_MAIOR_IGUAL reserv

                | VARIAVEL OP_REL_DUPLO_IGUAL INTEIRO
                | VARIAVEL OP_REL_DUPLO_IGUAL DOUBLE
                | VARIAVEL OP_REL_DUPLO_IGUAL VARIAVEL
                | VARIAVEL OP_REL_DUPLO_IGUAL reserv

                | reserv OP_REL_DUPLO_IGUAL INTEIRO
                | reserv OP_REL_DUPLO_IGUAL DOUBLE
                | reserv OP_REL_DUPLO_IGUAL VARIAVEL
                | reserv OP_REL_DUPLO_IGUAL reserv

                | VARIAVEL OP_REL_DIFERENTE INTEIRO
                | VARIAVEL OP_REL_DIFERENTE DOUBLE
                | VARIAVEL OP_REL_DIFERENTE VARIAVEL
                | VARIAVEL OP_REL_DIFERENTE reserv

                | reserv OP_REL_DIFERENTE INTEIRO
                | reserv OP_REL_DIFERENTE DOUBLE
                | reserv OP_REL_DIFERENTE VARIAVEL
                | reserv OP_REL_DIFERENTE reserv

                | VARIAVEL OP_REL_E INTEIRO
                | VARIAVEL OP_REL_E DOUBLE
                | VARIAVEL OP_REL_E VARIAVEL
                | VARIAVEL OP_REL_E reserv

                | reserv OP_REL_E INTEIRO
                | reserv OP_REL_E DOUBLE
                | reserv OP_REL_E VARIAVEL
                | reserv OP_REL_E reserv

                | VARIAVEL OP_REL_OU INTEIRO
                | VARIAVEL OP_REL_OU DOUBLE
                | VARIAVEL OP_REL_OU VARIAVEL
                | VARIAVEL OP_REL_OU reserv

                | reserv OP_REL_OU INTEIRO
                | reserv OP_REL_OU DOUBLE
                | reserv OP_REL_OU VARIAVEL
                | reserv OP_REL_OU reserv

    '''

def p_reserv(p):
    '''reserv : MOVER
               | MOVER_DIREITA
               | MOVER_ESQUERDA
               | MOVER_CIMA
               | MOVER_BAIXO
               | POSICAO_COBRA
               | POSICAO_ALIMENTO
               | PONTUACAO
               '''

def p_aux(p):
    'aux : AUX'

def p_impressao(p):
    '''impressao : PRINTF
                  | IMP'''

def p_true_false(p):
    '''true_false : TRUE
                   | FALSE
                   '''

def p_parametros_condicionais_grupo(p):
    '''
    cond_param : cond_param OP_REL_E cond_param
              | cond_param OP_REL_OU cond_param
    '''

def p_expressao_numero(p):
    '''
    expr : INTEIRO
        | DOUBLE
    '''

def p_expressao_variavel(p):
    '''
    expr : VARIAVEL
          | VARIAVEL OP_FINALLINHA
          | reserv
    '''

def p_expressao_operacao(p):
    '''
    expr : expr OP_MAT_MAIS expr
        |  expr OP_MAT_MENOS expr
        |  expr OP_MAT_VEZES expr
        |  expr OP_MAT_DIVIDE expr
        |  expr OP_MAT_MODULO expr
    '''

def p_expressao_grupo(p):
    '''
    expr : OP_PRIO_ABRE_PARENTESES expr OP_PRIO_FECHA_PARENTESES
    '''

def p_parametro_vazio(p):
    '''
    param_vazio :
    '''

def p_parametro(p):
    '''
    param : INTEIRO
        | DOUBLE
        | STRING
        | CHAR
        | VARIAVEL
        | reserv
    '''

def p_parametro_grupo(p):
    '''
    param : param OP_EXEC_VIRGULA param
    '''

def p_regra_funcao(p):
    '''
    funcao :  OP_PRIO_ABRE_PARENTESES param_vazio OP_PRIO_FECHA_PARENTESES
        |  OP_PRIO_ABRE_PARENTESES param OP_PRIO_FECHA_PARENTESES
    '''

def p_senao_se(p):
    '''
    senaose : ELIF OP_PRIO_ABRE_PARENTESES cond_param OP_PRIO_FECHA_PARENTESES OP_PRIO_ABRE_CHAVES statements OP_PRIO_FECHA_CHAVES
    '''

def p_senao_se_grupo(p):
    '''
    senaose : senaose senaose
            | senaose
    '''

errossintaticos = []
def p_error(p):
    errossintaticos.append(p)
    print("ERRO: ",p)

parser = yacc.yacc()

#Chamada do Algoritmo em si começa aqui
erros = 0

#função padrão para adicionar as classificações dos tokens para ser impressa pelo compilador
def add_lista_saida(t,notificacao):
    saidas.append((t.lineno,t.lexpos,t.type,t.value, notificacao))

saidas = []

#Aqui começa a execução do TkInter
root = tk.Tk() #cria a janela
class Application():
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.botoes()
        self.Menus()
        root.mainloop()

    def limpa_telaentrada(self):
        self.codigo_entry.delete(1.0, END)
        for i in self.saida.get_children():
            self.saida.delete(i)
        saidas.clear()
        erroslexicos.clear()
        errossintaticos.clear()
        global erros
        erros = 0
        self.frame_1.update()
        self.frame_2.update()
        root.update()

    def tela(self):
        self.root.title("Compilador")
        self.root.configure(background="white")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.minsize(width=550, height=350)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#DCDCDC",highlightbackground="grey", highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.07, relwidth=0.96, relheight=0.55)
        self.frame_2 = Frame(self.root, bd=4, bg="#DCDCDC",highlightbackground="grey", highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.70, relwidth=0.96, relheight=0.20)

    def chama_analisador(self):
        columns = ('linha', 'posicao', 'token', 'lexema', 'notificacao')
        self.saida = ttk.Treeview(self.frame_2, height=5, columns=columns, show='headings')
        self.saida.heading("linha", text='Linha')
        self.saida.heading("posicao", text='Posicao referente ao inicio da entrada')
        self.saida.heading("token", text='Token')
        self.saida.heading("lexema", text='Lexema')
        self.saida.heading("notificacao", text='Notificacao')

        data = self.codigo_entry.get(1.0, "end-1c")
        data.lower()
        lexer = lex.lex()
        lexer.input(data)

        # Tokenizar a entrada para passar para o analisador léxico
        for tok in lexer:
            global erros
            if tok.type == "string_mf":
                erros+=1
                add_lista_saida(tok,f"string mal formada")
            elif tok.type == "variavel_mf":
                erros+=1
                add_lista_saida(tok,f"variavel mal formada")
            elif tok.type == "numero_mf":
                erros+=1
                add_lista_saida(tok,f"numero mal formado")
            elif tok.type == "INTEIRO":
                max = (len(str(tok.value)))
                if (max > 15):
                    erros+=1
                    add_lista_saida(tok,f"entrada maior que a suportada")
                else:
                    add_lista_saida(tok, f" ")
            elif tok.type == "IF" or tok.type == "ELIF" or tok.type == "ELSE" or tok.type == "WHILE" or tok.type == "MOVER" or tok.type == "MOVER_DIREITA" or tok.type == "MOVER_ESQUERDA" or tok.type == "MOVER_CIMA" or tok.type == "MOVER_BAIXO" or tok.type == "POSICAO_COBRA" or tok.type == "POSICAO_ALIMENTO" or tok.type == "IFSULDEMINAS" or tok.type == "FOR" or tok.type == "PONTUACAO" or tok.type == "TRUE" or tok.type == "FALSE" or tok.type == "PRINTF" or tok.type == "AUX" or tok.type == "IMP":
                max = (len(tok.value))
                if (max < 20):
                    if tok.value in reserved:
                       tok.type = reserved[tok.value]
                       add_lista_saida(tok, f"palavra reservada")
                    else:
                        add_lista_saida(tok, f" ")
                else:
                    erros+=1
                    add_lista_saida(tok, f"Tamanho da Variavel maior que o suportado")
            else:
                add_lista_saida(tok, f" ")
        if (saidas[0][3] == "IFSULDEMINAS"):
            if (saidas[1][3] != "'"):
                erros += 1
                self.saida.insert('', tk.END, values="Algoritmo sem IFSULDEMINAS no início, condicao obrigatoria")
            else:
                pass
        else:
            erros += 1
            self.saida.insert('', tk.END, values="Algoritmo sem IFSULDEMINAS no início, condicao obrigatoria")

        for tok in erroslexicos:
            add_lista_saida(tok,f"Caracter Inválido nesta linguagem")

        tamerroslex = len(erroslexicos)
        if tamerroslex == 0 and erros == 0:
            self.saida.insert('', tk.END, values="Análise Léxica Concluída sem Erros")
            parser.parse(data)
            tamerrosin = len(errossintaticos)
            if tamerrosin == 0:
                self.saida.insert('', tk.END, values="Análise Sintática Concluída sem Erros")
            else:
                self.saida.insert('', tk.END, values="Erro Sintático")
        else:
            self.saida.insert('', tk.END, values="Erro Léxico")

        for retorno in saidas:
            self.saida.insert('', tk.END, values=retorno)

        self.saida.place(relx=0.001, rely=0.01, relwidth=0.999, relheight=0.95)

        self.scrollAnalise = ttk.Scrollbar(self.frame_2, orient='vertical',command=self.saida.yview)
        self.scrollAnalise.place(relx=0.979, rely=0.0192, relwidth=0.02, relheight=0.92)
        self.saida['yscrollcommand'] = self.scrollAnalise

    def botoes(self):
        # botao limpar
        self.bt_limpar = Button(text="Limpar", bd=2, bg="#FF6347", font=('', 11), command=self.limpa_telaentrada)
        self.bt_limpar.place(relx=0.74, rely=0.92, relwidth=0.1, relheight=0.05)

        # botao executar
        self.bt_executar = Button(text="Executar", bd=2, bg="lightgreen", font=('', 11), command=self.chama_analisador)
        self.bt_executar.place(relx=0.85, rely=0.92, relwidth=0.1, relheight=0.05)

        # criação da label e entrada do código
        self.lb_codigo = Label(text="Código Fonte", bg="white", font=('', 12))
        self.lb_codigo.place(relx=0.001, rely=-0.001, relwidth=0.2, relheight=0.07)

        # criação da label da analise lexica
        self.lb_analise = Label(text="Análise Léxica e Sintática", bg="white", font=('', 12))
        self.lb_analise.place(relx=0.001, rely=0.62, relwidth=0.2, relheight=0.07)

        self.codigo_entry = tk.Text(self.frame_1)
        self.codigo_entry.place(relx=0.001, rely=0.001, relwidth=0.995, relheight=0.995)

        self.scroll_bar = ttk.Scrollbar(self.frame_1, orient='vertical', command=self.codigo_entry.yview)
        self.scroll_bar.place(relx=0.982, rely=0.0019, relwidth=0.015, relheight=0.99)
        self.codigo_entry['yscrollcommand'] = self.scroll_bar

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        def onOpen():
            tf = fd.askopenfilename(
                initialdir="C:/Users/MainFrame/Desktop/",
                title="Open Text file",
                filetypes=(("Text Files", "*.txt"),)
            )
            tf = open(tf, 'r')
            entrada = tf.read()
            self.codigo_entry.insert(END, entrada)
            tf.close()

        def onSave():
            files = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            t = self.codigo_entry.get(0.0, END)
            files.write(t.rstrip())

        def tokens():
            newWindow = Toplevel(root)
            newWindow.title("Tabela de Tokens")
            newWindow.configure(background="white")
            newWindow.geometry("800x800")
            newWindow.resizable(True, True)
            newWindow.minsize(width=550, height=350)

            newWindow = ttk.Treeview(newWindow, height=3, column=('col1', 'col2', 'col3', 'col4'))
            newWindow.heading("#0", text='')
            newWindow.heading("#1", text='Tokens')
            newWindow.heading("#2", text='Lexemas')
            newWindow.heading("#3", text='Expressão Regular')
            newWindow.heading("#4", text='Descrição')

            newWindow.column("#0", width=1, stretch=NO)
            newWindow.column("#1", width=50, )
            newWindow.column("#2", width=200)
            newWindow.column("#3", width=125)
            newWindow.column("#4", width=125)

            newWindow.place(relx=0.001, rely=0.01, relwidth=0.999, relheight=0.95)

            newWindow.insert("", 1, text="", values=("ifsuldeminas", "ifsuldeminas", "ifsuldeminas", "Palavra Reservada ifsuldeminas"))
            newWindow.insert("", 2, text="", values=("posicao_cobra", "posicao_cobra", "posicao_cobra", "Palavra Reservada posicao_cobra"))
            newWindow.insert("", 3, text="", values=("posicao_alimento", "posicao_alimento", "posicao_alimento", "Palavra Reservada posicao_alimento"))
            newWindow.insert("", 4, text="", values=("mover", "mover", "mover", "Palavra Reservada mover"))
            newWindow.insert("", 5, text="", values=("mover_direita", "mover_direita", "mover_direita", "Palavra Reservada mover_direita"))
            newWindow.insert("", 6, text="", values=("mover_esquerda", "mover_esquerda", "mover_esquerda", "Palavra Reservada mover_esquerda"))
            newWindow.insert("", 7, text="", values=("mover_cima", "mover_cima", "mover_cima", "Palavra Reservada mover_cima"))
            newWindow.insert("", 8, text="", values=("mover_baixo", "mover_baixo", "mover_baixo", "Palavra Reservada mover_baixo"))
            newWindow.insert("", 9, text="", values=("pontuacao", "pontuacao", "pontuacao", "Palavra Reservada potuação"))
            newWindow.insert("", 10, text="", values=("imp", "imp", "imp", "Palavra Reservada imp"))

            newWindow.insert("", 11, text="", values=("if", "if", "if", "Palavra Reservada if"))
            newWindow.insert("", 12, text="", values=("elif", "elif", "elif", "Palavra Reservada elif"))
            newWindow.insert("", 13, text="", values=("else", "else", "else", "Palavra Reservada else"))
            newWindow.insert("", 14, text="", values=("for", "for", "for", "Palavra Reservada for"))
            newWindow.insert("", 15, text="", values=("while", "while", "while", "Palavra Reservada while"))
            newWindow.insert("", 16, text="", values=("printf", "printf", "printf", "Palavra Reservada printf"))
            newWindow.insert("", 17, text="", values=("true", "true", "true", "Palavra Reservada true"))
            newWindow.insert("", 18, text="", values=("false", "false", "false", "Palavra Reservada false"))
            newWindow.insert("", 19, text="", values=("aux", "aux", "aux", "Palavra Reservada aux"))

            newWindow.insert("", 20, text="", values=("op_mat_mais", "+", "+", "Operador Matemático mais"))
            newWindow.insert("", 21, text="", values=("op_mat_menos", "-", "-", "Operador Matemático menos"))
            newWindow.insert("", 22, text="", values=("op_mat_vezes", "*", "*", "Operador Matemático vezes"))
            newWindow.insert("", 23, text="", values=("op_mat_divide", "/", "/", "Operador Matemático divide"))
            newWindow.insert("", 24, text="", values=("op_mat_modulo", "%", "%", "Operador Matemático modulo"))

            newWindow.insert("", 25, text="", values=("op_prio_abre_parenteses", "(", "(", "Operador de Prioridade abre parenteses"))
            newWindow.insert("", 26, text="", values=("op_prio_fecha_parenteses", ")", ")", "Operador de Prioridade fecha parenteses"))
            newWindow.insert("", 27, text="", values=("op_prio_abre_chaves", "{", "{", "Operador de Prioridade abre chaves"))
            newWindow.insert("", 28, text="", values=("op_prio_fecha_chaves", "}", "}", "Operador de Prioridade fecha chaves"))
            newWindow.insert("", 29, text="", values=("op_prio_abre_colchetes", "[", "[", "Operador de Prioridade abre colchetes"))
            newWindow.insert("", 30, text="", values=("op_prio_fecha_colchetes", "]", "]", "Operador de Prioridade fecha colchetes"))

            newWindow.insert("", 31, text="", values=("op_rel_menor", "<", "<", "Operador Relacional menor"))
            newWindow.insert("", 32, text="", values=("op_rel_maior", ">", ">", "Operador Relacional maior"))
            newWindow.insert("", 33, text="", values=("op_rel_menor_igual", "<=", "<=", "Operador Relacional menor igual"))
            newWindow.insert("", 34, text="", values=("op_rel_maior_igual", ">=", ">=", "Operador Relacional maior igual"))
            newWindow.insert("", 35, text="", values=("op_rel_duplo_igual", "==", "==", "Operador Relacional duplo igual"))
            newWindow.insert("", 36, text="", values=("op_rel_diferente", "!=", "!=", "Operador Relacional diferente"))
            newWindow.insert("", 37, text="", values=("op_rel_e", "&", "&", "Operador Relacional e"))
            newWindow.insert("", 38, text="", values=("op_rel_ou", "|", "|", "Operador Relacional ou"))

            newWindow.insert("", 39, text="", values=("inteiro", "0,1,2,3,4,5,6,7,8,9", "0|1|2|3|4|5|6|7|8|9", "Dígito Númerico Inteiro"))
            newWindow.insert("", 40, text="", values=("double", "0.009...9.9999", "0.00|9.999", "Dígito Númerico Double"))
            newWindow.insert("", 41, text="", values=("char", "a,b,c...x,y,z", "a|b|c...x|y|z", "Char"))
            newWindow.insert("", 42, text="", values=("variavel", "char(char,inteiro)*", "[char]{1}[char|inteiro]{*}", "Variável Criada"))
            newWindow.insert("", 43, text="", values=("string", "qualquer entrada de texto", "[char]{1}[char|inteiro]{*}", "Entrada do tipo string"))

            newWindow.insert("", 44, text="", values=("op_exec_virgula", ",", ",", "Operador de Execução Vírgula"))
            newWindow.insert("", 45, text="", values=("op_exec_ponto_virgula", ";", ";", "Operador de Execução ponto e vírgula"))
            newWindow.insert("", 46, text="", values=("op_exec_dois_pontos", ":", ":", "Operador de Execução dois pontos"))
            newWindow.insert("", 47, text="", values=("op_exec_ponto", ".", ".", "Operador de Execução ponto"))

            newWindow.insert("", 48, text="", values=("op_imp_aspas", "'", "'", "Operação de Impressão aspa"))

            newWindow.insert("", 49, text="", values=("op_comentario", "#", "#", "Operador de Comentário"))
            newWindow.insert("", 50, text="", values=("op_finallinha", "'", "'", "Operador de Final de Linha"))

            newWindow.insert("", 51, text="", values=("op_atrib_negacao", "~", "~", "Operador de Atribuição negação"))
            newWindow.insert("", 52, text="", values=("op_atri_igual", "=", "=", "Comando de Atribuição igual"))
            newWindow.insert("", 53, text="", values=("op_atri_mais_igual", "+=", "+=", "Comando de Atribuição mais igual"))
            newWindow.insert("", 54, text="", values=("op_atri_menos_igual", "-=", "-=", "Comando de Atribuição menos igual"))
            newWindow.insert("", 55, text="", values=("op_atri_vezes_igual", "*=", "*=", "Comando de Atribuição vezes igual"))
            newWindow.insert("", 56, text="", values=("op_atri_divide_igual", "/=", "/=", "Comando de Atribuição divide igual"))

            label.pack(pady=10)
            mainloop()

        menubar.add_cascade(label="Arquivo", menu=filemenu)
        menubar.add_cascade(label="Tabela de Tokens", menu=filemenu2)

        filemenu.add_command(label="Abrir Script", command=onOpen)
        filemenu.add_command(label="Salvar Como", command=onSave)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Tokens", command=tokens)

Application()