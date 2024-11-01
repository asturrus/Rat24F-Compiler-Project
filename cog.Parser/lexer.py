import re

# Tokens defined as regular expressions

real = r'\d+\.\d+'
int = r'\d+'
identifier = r'[a-zA-Z][a-zA-Z0-9]*'
keyword = r'\b(?:while|if|integer|else|fi|return|get|put|true|false|boolean|real|function)\b'
separator = r'[\(\){};,\[\]@]'
operator = r'<=|>=|!=|==|[+\-*/=<>|]'


token_types = '|'.join([real, int, identifier, operator, separator])        # conjoined list of all token types (regex)

def analyze(input):

    file = open(input, "r") #OPEN A FILENAME
    token_collection = [] # Collection of tokens from file read
    with file:
        for line in file:

            cleaned_line = re.sub(r'//.*|\[\*.*?\*\]', '', line).strip()        # cleaning the line of comments and whitespace

            line_tokens = re.findall(token_types, cleaned_line)      # all tokens on a single line

            token_collection.extend(line_tokens)        # add all tokens found to the collection

    return [token for token in token_collection if token.strip()] # returning the tokens found


def classify_token(tokens):
    specified_tokens = []

# DFSM to figure out each individual token to its respective lexeme and return that list of specified tokens
    for i in range(len(tokens)):
        if re.fullmatch(keyword, tokens[i]):
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

# Read the input file analyze it and classify the tokens into a list
    input_file = input("Input a valid test file ending in .txt: ")
    tokens = analyze(input_file)

    specified_tokens = classify_token(tokens)

# Print statement printing out token then lexeme respectively from the specified token list

    print("\n")
    print (f'{"token":5} {"":20} {"lexeme":6}')
    print (f'{"-"*33}')
    for token, lexeme in specified_tokens:
        print(f'{token:10} {"":16} {lexeme:11}')


if __name__ == "__main__":
    main()