import re

# Tokens defined as regular expressions
real = r'\d+\.\d+'
integer = r'\d+'
identifier = r'[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]|[a-zA-Z]'
keyword = r'\b(?:while|if|integer|else|fi|return|get|put|true|false|boolean|real|function)\b'
separator = r'[\(\){};,\[\]@]'
operator = r'<=|>=|!=|==|[+\-*/=<>|]'

# Combined regex pattern for all token types
token_types = '|'.join([real, integer, identifier, keyword, separator, operator])

def analyze(input_text):
    """Tokenize the input text and return a list of tokens with line numbers."""
    token_collection = []
    lines = input_text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        cleaned_line = re.sub(r'//.*|\[\*.*?\*\]', '', line).strip()  # Remove comments and whitespace
        line_tokens = re.findall(token_types, cleaned_line)
        for token in line_tokens:
            token_collection.append((token, line_number))
    return token_collection

def classify_token(tokens):
    """Classify each token and return a list of (type, lexeme, line) tuples."""
    specified_tokens = []
    for lexeme, line_number in tokens:
        if re.fullmatch(keyword, lexeme):
            specified_tokens.append(("keyword", lexeme, line_number))
        elif re.fullmatch(separator, lexeme):
            specified_tokens.append(("separator", lexeme, line_number))
        elif re.fullmatch(integer, lexeme):
            specified_tokens.append(("integer", lexeme, line_number))
        elif re.fullmatch(real, lexeme):
            specified_tokens.append(("real", lexeme, line_number))
        elif re.fullmatch(identifier, lexeme):
            specified_tokens.append(("identifier", lexeme, line_number))
        elif re.fullmatch(operator, lexeme):
            specified_tokens.append(("operator", lexeme, line_number))
    return specified_tokens

def get_tokens(input_text):
    """Yield classified tokens with line numbers for the parser."""
    tokens = analyze(input_text)
    specified_tokens = classify_token(tokens)
    for token_type, lexeme, line in specified_tokens:
        yield token_type, lexeme, line
