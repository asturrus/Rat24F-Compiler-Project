# Anthony Sturrus, Carlos Lopez,

import re

int = r'\d+'
real = r'\d+\.\d+'
identifier = r'[a-z][a-z0-9]*'
keyword =
# separator =
operator = ["+", "-", "/", "*", "=", "<", ">", "=>", "=<"]


token_types = '|'.join([int, real, identifier, operator, keyword, separator])

def analyze(input):

    file = open(input, "r") #OPEN A FILENAME
    token_collection = []
    with file:
        for line in file:

            cleaned_line = re.sub(r'//.*|\[\*.*?\*\]', '', line).strip()        # cleaning the line of comments and whitespace

            line_tokens = re.findall(token_types, cleaned_line)      # all tokens on a single line

            token_collection.extend(line_tokens)        # add all tokens found to the collection

    return token_collection


def main():

    input_file = input("Input a valid test file ending in .txt: ")
    tokens = analyze(input_file)

    tokens = [token for token in tokens if tokens]

    specified_tokens = []

    is_id = False
    temp = ""

    for i in range(len(tokens)):
        if is_id and tokens[i] != '"':
            temp = temp + " " + tokens[i]
            continue
        if tokens[i] == '"':
            if is_id:
                specified_tokens.append([temp.strip(), "string literal"]) #NOT SURE ON STRING LITERAL TOKEN
            is_id = not is_id
            specified_tokens.append(tokens[i], "operator")
        elif re.match(separator, tokens[i]):
            specified_tokens.append(tokens[i], "separator")

        elif re.match(operator, tokens[i]):
            specified_tokens.append(tokens[i], "operator")

        elif re.match(keyword, tokens[i]):
            specified_tokens.append(tokens[i], "keyword")

        elif re.match(int, tokens[i]):
            specified_tokens.append(tokens[i], "integer")

        elif re.match(identifier, tokens[i]):
            specified_tokens.append(tokens[i], "identifier")

        elif re.match(real, tokens[i]):
            specified_tokens.append(tokens[i], "real")

    print (f'{"token":5} {"":20} {"lexeme":6}')
    print (f'{"-":31}')
    for token, lexeme in specified_tokens:
        print(f'{token:10} {"":10} {lexeme:11}')
