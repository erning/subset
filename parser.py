# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME',
    'GT', 'LT', 'EQ', 'GTE', 'LTE', 'NE',
    'OR', 'AND', 'NOT',
    'LPAREN', 'RPAREN',
    'INTEGER', 'FLOAT', 'STRING'
)

precedence = (
    ('left',  'OR'),
    ('left',  'AND'),
    ('right', 'NOT')
)

def t_STRING(t):
    r'(("[^"]*")' "|('[^']*'))"
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    return t

def t_INTEGER(t):
    r'\d+'
    return t

def t_GTE(t):
    r'>=|=>'
    t.value = '>='
    return t

def t_LTE(t):
    r'<=|=<'
    t.value = '<='
    return t

def t_NE(t):
    r'!=|<>'
    t.value = '!='
    return t

def t_GT(t):
    r'>'
    return t

def t_LT(t):
    r'<'
    return t

def t_EQ(t):
    r'==|='
    t.value = '=='
    return t

def t_OR(t):
    r'(\|\|)|([oO][rR])'
    t.value = '||'
    return t

def t_AND(t):
    r'(&&)|([aA][nN][dD])'
    t.value = '&&'
    return t

def t_NOT(t):
    r'(!)|([nN][oO][tT])'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_NAME(t):
    r'([a-zA-Z][a-zA-Z_0-9]*)|([a-zA-Z_][a-zA-Z0-9]+)'
    return t

def t_error(t):
    raise Exception("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t\r\n'

lexer = lex.lex()

'''
expr    : factor
        | NOT expr
        | expr AND expr
        | expr OR expr
        | LPAREN expr RPAREN

factor  : nfactor
        | sfactor

nfactor : NAME EQ number
        | NAME NE number
        | NAME GT number
        | NAME LT number
        | NAME GTE number
        | NAME LTE number
        | number EQ NAME
        | number NE NAME
        | number GT NAME
        | number LT NAME
        | number GTE NAME
        | number LTE NAME

number  : INTEGER
        | FLOAT

sfactor : NAME EQ STRING
        | NAME NE STRING
        | STRING EQ NAME
        | STRING NE NAME

'''

op_not = {
    '||': '&&',
    '&&': '||',
    '>' : '<=',
    '<' : '>=',
    '==': '!=',
    '>=': '<',
    '<=': '>',
    '!=': '=='
}

op_swap = {
    '>' : '<',
    '<' : '>',
    '==': '==',
    '>=': '<=',
    '<=': '>=',
    '!=': '!='
}

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

def p_expr_NOT(t):
    '''
    expr    : NOT expr
    '''
    def logical_not(expr):
        if type(expr) is not tuple:
            return expr
        left, op, right = expr
        return logical_not(left), op_not[op], logical_not(right)
    t[0] = logical_not(t[2])

def p_expr_AND(t):
    '''
    expr    : expr AND expr
    '''
    t[0] = (t[1], t[2], t[3])

def p_expr_OR(t):
    '''
    expr    : expr OR expr
    '''
    t[0] = (t[1], t[2], t[3])

def p_expr_parenthesized(t):
    '''
    expr    : LPAREN expr RPAREN
    '''
    t[0] = t[2]

def p_expr_factor(t):
    '''
    expr    : factor
    '''
    t[0] = t[1]

def p_factor(t):
    '''
    factor  : nfactor
            | sfactor
    '''
    t[0] = t[1]

def p_nfactor(t):
    '''
    nfactor : NAME EQ number
            | NAME NE number
            | NAME GT number
            | NAME LT number
            | NAME GTE number
            | NAME LTE number
    '''
    t[0] = (t[1], t[2], t[3])

def p_nrfactor(t):
    '''
    nfactor : number EQ NAME
            | number NE NAME
            | number GT NAME
            | number LT NAME
            | number GTE NAME
            | number LTE NAME
    '''
    t[0] = (t[3], op_swap[t[2]], t[1])

def p_number(t):
    '''
    number  : INTEGER
            | FLOAT
    '''
    if '.' in t[1]:
        t[0] = float(t[1])
    else:
        t[0] = int(t[1])

def p_sfactor(t):
    '''
    sfactor : NAME EQ STRING
            | NAME NE STRING
    '''
    t[0] = (t[1], t[2], t[3][1:-1])

def p_srfactor(t):
    '''
    sfactor : STRING EQ NAME
            | STRING NE NAME
    '''
    t[0] = (t[3][1:-1], t[2], t[1])


def p_error(p):
    raise Exception("Syntax error in input!")

parser = yacc.yacc()

parse = parser.parse

__all__ = ['parse']
