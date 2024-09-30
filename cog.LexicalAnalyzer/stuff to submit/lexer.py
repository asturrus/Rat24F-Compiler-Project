# Anthony Sturrus, Carlos Lopez,

import re

real = r'\d+\.\d+'
int = r'\d+'
identifier = r'[a-zA-Z][a-zA-Z0-9]*'
keyword = {"while", "if", "integer", "else", "fi", "return", "get", 
           "put", "true", "false", "boolean", "real", "function",}
separator = r'[\(\){};,\[\]@]'
operator = r'<=|>=|!=|==|[+\-*/=<>|]'


token_types = '|'.join([real, int, identifier, operator, separator])

def analyze(input):

    file = open(input, "r") #OPEN A FILENAME
    token_collection = []
    with file:
        for line in file:

            cleaned_line = re.sub(r'//.*|\[\*.*?\*\]', '', line).strip()        # cleaning the line of comments and whitespace

            line_tokens = re.findall(token_types, cleaned_line)      # all tokens on a single line

            token_collection.extend(line_tokens)        # add all tokens found to the collection

    return [token for token in token_collection if token.strip()]



def classify_token(tokens): 
    specified_tokens = []
    is_string_literal = False
    temp = ""

    for i in range(len(tokens)):
        if is_string_literal:
            if tokens[i] != '"':
                temp += " " + tokens[i]
            else:
                # Close the string literal
                specified_tokens.append((temp.strip(), "string literal"))
                temp = ""
                is_string_literal = False
        elif tokens[i] == '"':
            is_string_literal = True
        elif tokens[i] in keyword:
            specified_tokens.append(("keyword", tokens[i]))
        elif re.fullmatch(separator, tokens[i]):
            specified_tokens.append(("separator", tokens[i]))
        elif re.fullmatch(int, tokens[i]):
            specified_tokens.append(("integer", tokens[i]))
        elif re.fullmatch(real, tokens[i]):
            specified_tokens.append(("real", tokens[i]))
        elif re.fullmatch(identifier, tokens[i]):
            specified_tokens.append(("identifier", tokens[i]))
        elif re.fullmatch(operator, tokens[i]):
            specified_tokens.append(("operator", tokens[i]))

    return specified_tokens



def main():

    input_file = input("Input a valid test file ending in .txt: ")
    tokens = analyze(input_file)

    #tokens = [token for token in tokens if tokens]

    specified_tokens = classify_token(tokens)

    print (f'{"token":5} {"":20} {"lexeme":6}')
    print (f'{"-":31}')
    for token, lexeme in specified_tokens:
        print(f'{token:10} {"":10} {lexeme:11}')


if __name__ == "__main__":
    main()