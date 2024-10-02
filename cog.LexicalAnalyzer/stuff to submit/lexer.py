# Anthony Sturrus, Carlos Lopez,

import re

real = r'\d+\.\d+'
int = r'\d+'
identifier = r'[a-zA-Z][a-zA-Z0-9]*'
keyword = r'\b(?:while|if|integer|else|fi|return|get|put|true|false|boolean|real|function)\b'
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

<<<<<<< Updated upstream
=======
def main():

    input_filename = input("Input a valid test file ending in .txt: ")
    tokens = analyze(input_filename)

    tokens = [token for token in tokens if token]
>>>>>>> Stashed changes


def classify_token(tokens): 
    specified_tokens = []
    #temp = ""
    #is_id = False

    for i in range(len(tokens)):
<<<<<<< Updated upstream
        # if is_id and tokens[i] != '"':
        #     temp += " " + tokens[i]
        #     continue
        # if tokens[i] == '"':
        #     if is_id:
        #         # Close the string literal
        #         specified_tokens.append((temp.strip(), "string literal"))
        #     is_id = not is_id
        #     specified_tokens.append((tokens[i], "operator"))
        
        if tokens[i] == '"' :
            raise ValueError("Error: Quotes aren't apart of syntax rules")

        elif re.fullmatch(keyword, tokens[i]):
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
=======
        if is_id and tokens[i] != '"':
            temp = temp + " " + tokens[i]
            continue
        if tokens[i] == '"':
            if is_id:
                specified_tokens.append([temp.strip(), "string literal"]) # NOT SURE ON STRING LITERAL TOKEN
            is_id = not is_id
            specified_tokens.append([tokens[i], "operator"])




        elif re.match(separator, tokens[i]):
            specified_tokens.append([tokens[i], "separator"])
>>>>>>> Stashed changes


<<<<<<< Updated upstream

def main():

    input_file = input("Input a valid test file ending in .txt: \n")
    tokens = analyze(input_file)

    #tokens = [token for token in tokens if tokens]

    specified_tokens = classify_token(tokens)
=======
            actions = re.findall(r'\b\w{2,}\b|.', tokens[i])
            for action in actions:
                specified_tokens.append([action, "operator"])

        elif re.match(keyword, tokens[i]):
            specified_tokens.append([tokens[i], "keyword"])

        elif re.match(int, tokens[i]):
            specified_tokens.append([tokens[i], "integer"])

        elif re.match(identifier, tokens[i]):
            specified_tokens.append([tokens[i], "identifier"])

        elif re.match(real, tokens[i]):
            specified_tokens.append([tokens[i], "real"])
>>>>>>> Stashed changes

    print (f'{"token":5} {"":20} {"lexeme":6}')
    print (f'{"-"*35}')
    for token, lexeme in specified_tokens:
        print(f'{token:10} {"":16} {lexeme:11}')


if __name__ == "__main__":
    main()