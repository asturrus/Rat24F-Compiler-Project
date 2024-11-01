from lexer import *

switch = True

def rat24F():
    if switch:
        print("<INPUTRULE>::= .... ")
        # opt_function_def()
        if token == '@':
            lexer()
        else ("@ expected"):

        opt_dl()
        statement_list()
        if token == "@"