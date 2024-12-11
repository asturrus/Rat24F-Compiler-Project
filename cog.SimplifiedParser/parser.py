from lexer import get_tokens
import sys

# Globals to hold the current token, lexeme, and token generator
current_token = None
current_lexeme = None
line_number = None
previous_line_number = None
token_generator = None
lines = []  # List to hold each line of code for reference
memory_address = 9000
instr_add = 1

# Assembly Instruction Stack Array

# def back_patch(jump_addr):
#     addr = jumpstack.pop()
#     instructions[] = jump_addr

def back_patch(jump_addr):
    global instructions
    for i, instruction in enumerate(instructions):
        if ("JUMPZ" in instruction and "None" in instruction) or ("JUMP" in instruction and "None" in instruction):
            # Split the instruction to extract and modify the operand
            parts = instruction.split()
            parts[-1] = str(jump_addr)  # Replace 'None' with the jump address
            instruction[i] = " ".join(parts)
            break

instructions = []

def gen_instr(op, oprnd):
    global instr_add
    if oprnd is not None:
        instructions.append(f"{instr_add}: {op} {oprnd}")
    else:
        instructions.append(f"{instr_add}: {op}")
    instr_add += 1

# JumpStack

jumpstack = []

# Symbol Table Handling

symbol_table = {}

def add_symbol():
    global memory_address
    if current_token == "identifier" and current_lexeme not in symbol_table:
        symbol_table.update({current_lexeme : memory_address})
        memory_address += 1

def print_assem_instruct():
    # for i in range(len(instructions) - 1, -1, -1):
    for i in instructions:
        print(i)

def print_sym_table():
    print(f'{"Symbol":7}{"":10}{"Memory Address":18}{"Type":7}''\n')
    for i in symbol_table:
        print(f'{i:7}{"":8}{symbol_table[i]:6}{"":13}{"Integer":7}')

switch = False  # Toggle to control production rule printing


def next_token():
# Get the next token from the lexer, print it, and detect line changes
    global current_token, current_lexeme, line_number
    try:
        current_token, current_lexeme, line_number = next(token_generator)

        if current_token == "integer":
            gen_instr("PUSHI", current_lexeme)

        add_symbol() # Add each unique identifier to the symbol table

    except StopIteration:
        current_token, current_lexeme, line_number = 'EOF', 'EOF', -1


def error(expected):
    if current_token == 'unknown':
        print(f"Syntax Error: Unknown symbol '{current_lexeme}' at line {line_number}")
        sys.exit(1)
    else:
        print(f"Syntax Error: Expected {expected}, but got {current_token} ('{current_lexeme}') at line {line_number}")
        sys.exit(1)

# Grammar functions based on each rule

def rat24F():
    if switch:
        print("<Rat24F> ::= <Opt Function Definitions> @ <Opt Declaration List> <Statement List> @")
    opt_function_definitions()
    if current_token == 'separator' and current_lexeme == '@':
        next_token()
    else:
        error("@")
    opt_declaration_list()
    statement_list()
    if current_token == 'separator' and current_lexeme == '@':
        next_token()
    else:
        error("@")

def opt_function_definitions():
    if switch:
        print("<Opt Function Definitions> ::= <Function Definitions> | <Empty>")
    if current_token == 'keyword' and current_lexeme == 'function':
        function_definitions()
    # epsilon case (do nothing)

def function_definitions():
    if switch:
        print("<Function Definitions> ::= <Function> <Function Definitions Prime>")
    function()
    function_definitions_prime()

def function_definitions_prime():
    if switch:
        print("<Function Definitions Prime> ::= <Function Definitions> | ε")
    if current_token == 'keyword' and current_lexeme == 'function':
        function_definitions()

def function():
    if switch:
        print("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    if current_token == 'keyword' and current_lexeme == 'function':
        next_token()
        if current_token == 'identifier':
            next_token()
            if current_token == 'separator' and current_lexeme == '(':
                next_token()
                opt_parameter_list()
                if current_token == 'separator' and current_lexeme == ')':
                    next_token()
                    opt_declaration_list()
                    body()
                else:
                    error(")")
            else:
                error("(")
        else:
            error("Identifier")
    else:
        error("function")

def opt_parameter_list():
    if switch:
        print("<Opt Parameter List> ::= <Parameter List> | <Empty>")
    if current_token == 'identifier':
        parameter_list()

def parameter_list():
    if switch:
        print("<Parameter List> ::= <Parameter> <Parameter List Prime>")
    parameter()
    parameter_list_prime()

def parameter_list_prime():
    if switch:
        print("<Parameter List Prime> ::= , <Parameter List> | ε")
    if current_token == 'separator' and current_lexeme == ',':
        next_token()
        parameter_list()

def parameter():
    if switch:
        print("<Parameter> ::= <IDs> <Qualifier>")
    ids()
    qualifier()

def qualifier():
    if switch:
        print("<Qualifier> ::= integer | boolean | real")
    if current_lexeme in ['integer', 'boolean', 'real']:
        next_token()
    else:
        error("qualifier (integer, boolean, real)")

def body():
    if switch:
        print("<Body> ::= { <Statement List> }")
    if current_token == 'separator' and current_lexeme == '{':
        next_token()
        statement_list()
        if current_token == 'separator' and current_lexeme == '}':
            next_token()
        else:
            error("}")
    else:
        error("{")

def opt_declaration_list():
    if switch:
        print("<Opt Declaration List> ::= <Declaration List> | <Empty>")
    if current_lexeme in ['integer', 'boolean', 'real']:
        declaration_list()

def declaration_list():
    if switch:
        print("<Declaration List> ::= <Declaration> ; <Declaration List Prime>")
    declaration()
    if current_token == 'separator' and current_lexeme == ';':
        next_token()
        declaration_list_prime()
    else:
        error(";")

def declaration_list_prime():
    if switch:
        print("<Declaration List Prime> ::= <Declaration List> | ε")
    if current_lexeme in ['integer', 'boolean', 'real']:
        declaration_list()

def declaration():
    if switch:
        print("<Declaration> ::= <Qualifier> <IDs>")
    qualifier()
    ids()

def ids():
    if switch:
        print("<IDs> ::= <Identifier> | <Identifier>, <IDs>")
    if current_token == 'identifier':
        next_token()
        if current_token == 'separator' and current_lexeme == ',':
            next_token()
            ids()
    else:
        error("Identifier")

def statement_list():
    if switch:
        print("<Statement List> ::= <Statement> <Statement List Prime>")
    statement()
    statement_list_prime()

def statement_list_prime():
    if switch:
        print("<Statement List Prime> ::= <Statement List> | ε")
    if current_token in {'identifier', 'separator', 'keyword'}:
        if current_token == 'identifier' or current_lexeme in {'{', 'if', 'return', 'put', 'get', 'while'}:
            statement_list()  # Recurse for additional statements
    # epsilon case: do nothing if no more statements

def statement():
    if switch:
        print("<Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    if current_token == 'separator' and current_lexeme == '{':
        compound()
    elif current_token == 'identifier':
        assign()
    elif current_token == 'keyword' and current_lexeme == 'if':
        if_statement()
    elif current_token == 'keyword' and current_lexeme == 'return':
        return_statement()
    elif current_token == 'keyword' and current_lexeme == 'put':
        print_statement()
    elif current_token == 'keyword' and current_lexeme == 'get':
        scan_statement()
    elif current_token == 'keyword' and current_lexeme == 'while':
        while_statement()
    else:
        error("Statement")

def compound():
    if switch:
        print("<Compound> ::= { <Statement List> }")
    if current_token == 'separator' and current_lexeme == '{':
        next_token()
        statement_list()
        if current_token == 'separator' and current_lexeme == '}':
            next_token()
        else:
            error("}")

def assign():
    if switch:
        print("<Assign> ::= <Identifier> = <Expression> ;")
    if current_token == 'identifier':
        save = current_lexeme
        next_token()
        if current_token == 'operator' and current_lexeme == '=':
            next_token()
            expression()
            gen_instr("POPM", symbol_table[save])

            if current_token == 'separator' and current_lexeme == ';':
                next_token()
            else:
                error(";")
        else:
            error("=")
    else:
        error("Identifier")

def if_statement():
    if switch:
        print("<If> ::= if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> else <Statement> fi")
    if current_lexeme == 'if':
        next_token()
        if current_token == 'separator' and current_lexeme == '(':
            next_token()
            condition()
            if current_token == 'separator' and current_lexeme == ')':
                next_token()
                statement()
                back_patch(instr_add)
                if current_lexeme == 'fi':
                    next_token()
                elif current_lexeme == 'else':
                    next_token()
                    statement()
                    if current_lexeme == 'fi':
                        next_token()
                    else:
                        error("fi")
                else:
                    error("fi or else")
            else:
                error(")")
        else:
            error("(")
    else:
        error("if")

def return_statement():
    if switch:
        print("<Return> ::= return ; | return <Expression> ;")
    if current_lexeme == 'return':
        next_token()
        if current_token == 'separator' and current_lexeme == ';':
            next_token()
        else:
            expression()
            if current_token == 'separator' and current_lexeme == ';':
                next_token()
            else:
                error(";")

def print_statement():
    if switch:
        print("<Print> ::= put ( <Expression> );")
    if current_lexeme == 'put':
        next_token()
        if current_token == 'separator' and current_lexeme == '(':
            next_token()
            expression()
            if current_token == 'separator' and current_lexeme == ')':
                next_token()
                if current_token == 'separator' and current_lexeme == ';':
                    next_token()
                    gen_instr("STDOUT", None)
                else:
                    error(";")
            else:
                error(")")
        else:
            error("(")

def scan_statement():
    if switch:
        print("<Scan> ::= get ( <IDs> );")
    if current_lexeme == 'get':
        gen_instr("STDIN", None)
        next_token()
        if current_token == 'separator' and current_lexeme == '(':
            next_token()
            gen_instr("POPM", symbol_table[current_lexeme])
            ids()
            if current_token == 'separator' and current_lexeme == ')':
                next_token()
                if current_token == 'separator' and current_lexeme == ';':
                    next_token()
                else:
                    error(";")
            else:
                error(")")
        else:
            error("(")

def while_statement():
    global instr_add
    if switch:
        print("<While> ::= while ( <Condition> ) <Statement>")
    if current_lexeme == 'while':
        address = instr_add
        gen_instr("LABEL", None)
        next_token()
        if current_token == 'separator' and current_lexeme == '(':
            next_token()
            condition()
            if current_token == 'separator' and current_lexeme == ')':
                next_token()
                statement()
                gen_instr("JUMP", address)
                back_patch(instr_add)
            else:
                error(")")
        else:
            error("(")

def condition():
    if switch:
        print("<Condition> ::= <Expression> <Relop> <Expression>")
    expression()
    relop()
    expression()

def relop():
    if switch:
        print("<Relop> ::= == | != | > | < | <= | =>")
    if current_lexeme in ['==', '!=', '>', '<', '<=', '=>']:

        if current_lexeme == "<":
            gen_instr("LES", None)
            jumpstack.append(instr_add)
            gen_instr("JUMPZ", None)

        if current_lexeme == ">":
            gen_instr("GRT", None)
            jumpstack.append(instr_add)
            gen_instr("JUMPZ", None)

        if current_lexeme == "!=":
            gen_instr("NEQ", None)
            jumpstack.append(instr_add)
            gen_instr("JUMPZ", None)

        if current_lexeme == "==":
            gen_instr("EQU", None)
            jumpstack.append(instr_add)
            gen_instr("JUMPZ", None)

        if current_lexeme == "=>":
            gen_instr("GEQ", None)
            jumpstack.append(instr_add)
            gen_instr("JUMPZ", None)

        if current_lexeme == "<=":
            gen_instr("LEQ", None)
            jumpstack.append(instr_add)
            gen_instr("JUMPZ", None)


        next_token()
    else:
        error("relational operator")

def expression():
    if switch:
        print("<Expression> ::= <Term> <Expression Prime>")
    term()
    expression_prime()

def expression_prime():
    if switch:
        print("<ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | ε")
    if current_lexeme in ['+', '-']:

        if current_lexeme == '+':
            next_token()
            term()
            gen_instr("ADD", None)

        else:
            next_token()
            term()
            gen_instr("SUB", None)

        expression_prime()

def term():
    if switch:
        print("<Term> ::= <Factor> <Term Prime>")
    factor()
    term_prime()

def term_prime():
    if switch:
        print("<TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | ε")
    if current_lexeme in ['*', '/']:

        if current_lexeme == '*':
            next_token()
            factor()
            gen_instr("MUL", None)

        else:
            next_token()
            factor()
            gen_instr("DIV", None)

        term_prime()

def factor():
    if switch:
        print("<Factor> ::= - <Primary> | <Primary>")
    if current_lexeme == '-':
        next_token()
        primary()
    else:
        primary()

def primary():
    if switch:
        print("<Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false")
    if current_token == 'identifier':
        gen_instr("PUSHM", symbol_table[current_lexeme])
        next_token()
        if current_token == 'separator' and current_lexeme == '(':
            next_token()
            ids()
            if current_token == 'separator' and current_lexeme == ')':
                next_token()
            else:
                error(")")
    elif current_token == 'integer':
        next_token()
    elif current_token == 'real':
        next_token()
    elif current_lexeme == 'true' or current_lexeme == 'false':
        next_token()
    elif current_token == 'separator' and current_lexeme == '(':
        next_token()
        expression()
        if current_token == 'separator' and current_lexeme == ')':
            next_token()
        else:
            error(")")
    else:
        error("primary")

def parse(input_text):
    global token_generator, lines, memory_address
    lines = input_text.splitlines()  # Store each line of the input for reference
    token_generator = get_tokens(input_text)
    next_token()  # Initialize with the first token
    rat24F()


    if current_token == 'EOF':
        print("\nParsing complete: no syntax errors.")
    else:
        error("EOF (end of file)")

def main():
    filename = input("Input a test file ending in .txt: ")
    try:
        with open(filename, 'r') as file:
            input_text = file.read()
        parse(input_text)

        print_assem_instruct()

        print_sym_table()

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")



if __name__ == "__main__":
    main()