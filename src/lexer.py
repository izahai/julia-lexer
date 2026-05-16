import re

# Define the token categories using regular expressions (Regex)
TOKEN_RULES = [
    # 1. Comments (To be ignored, but tracked)
    ('COMMENT',     r'#.*'),
    
    # 2. Keywords (Specific words reserved by Julia)
    ('KEYWORD',     r'\b(function|end|if|elseif|else|while|for|in|return|global)\b'),
    
    # 3. Literals (Data values)
    ('FLOAT',       r'\b\d+\.\d+\b'),         # Matches numbers like 3.14
    ('INT',         r'\b\d+\b'),              # Matches integers like 42 or 0
    ('STRING',      r'"[^"\\]*(?:\\.[^"\\]*)*"'), # Matches text inside double quotes
    
    # 4. Identifiers (Variable and function names)
    ('IDENTIFIER',  r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    
    # 5. Operators (Mathematical and logical)
    ('OPERATOR',    r'(>=|<=|==|!=|\+|-|\*|/|=|:|>|<)'),
    
    # 6. Punctuation & Delimiters
    ('PUNCTUATION', r'[\(\),\[\]\{\}]'),
    
    # 7. Whitespace (Spaces, tabs, newlines to be skipped)
    ('SKIP',        r'[ \t\n\r]+'),
    
    # 8. Mismatched/Illegal characters (For error handling)
    ('MISMATCH',    r'.'),
]

# Combine all rules into one massive regular expression master-pattern
MASTER_REGEX = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_RULES))

def tokenize(code_text):
    """
    Scans through the provided text string and breaks it into a list of tuples:
    [(TOKEN_TYPE, VALUE, LINE_NUMBER), ...]
    """
    tokens = []
    line_num = 1
    line_start = 0
    
    # Scan through the code using our master regular expression
    for match in MASTER_REGEX.finditer(code_text):
        kind = match.lastgroup
        value = match.group(kind)
        column = match.start() - line_start + 1
        
        if kind == 'SKIP':
            # Count newlines to keep track of line numbers for debugging
            if '\n' in value:
                line_num += value.count('\n')
                # FIX: Precise Column Tracking Math
                # Track the exact index position of the absolute last newline character observed
                line_start = match.start() + value.rfind('\n') + 1
        elif kind == 'COMMENT':
            # Skip comments entirely
            continue
        elif kind == 'MISMATCH':
            # If we hit something the lexer doesn't recognize, throw an error
            raise SyntaxError(f"Lexer Error: Illegal character '{value}' at line {line_num}, column {column}")
        else:
            # Add the valid token to our output list
            tokens.append((kind, value, line_num))
            
    return tokens