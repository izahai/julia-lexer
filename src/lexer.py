import re

# ---------------------------------------------------------------------------
# Token Rules – ordered by priority (first match wins inside MASTER_REGEX)
# ---------------------------------------------------------------------------
TOKEN_RULES = [
    # 1. Block comments  #= ... =#  (handled separately – see tokenize())
    #    We use a sentinel here so the master regex "sees" the open marker.
    ('BLOCK_COMMENT_START', r'#='),

    # 2. Single-line comments
    ('COMMENT',     r'#.*'),

    # 3. Keywords
    ('KEYWORD',     r'\b(function|end|if|elseif|else|while|for|in|return|global|local|'
                    r'const|begin|let|do|try|catch|finally|throw|import|using|export|'
                    r'module|struct|mutable|abstract|type|where|macro|quote|true|false|nothing)\b'),

    # 4. Literals
    ('FLOAT',       r'\b\d+\.\d+([eE][+-]?\d+)?\b'),
    ('INT',         r'\b\d+\b'),
    # String with interpolation marker — full match, subdivided in post-processing
    ('STRING',      r'"[^"\\]*(?:\\.[^"\\]*)*"'),

    # 5. Symbol literals  :identifier  or  :operator-combo
    ('SYMBOL',      r':[a-zA-Z_][a-zA-Z0-9_]*|:(?:>=|<=|==|!=|\+=|-=|\*=|/=|\+|-|\*|/|>|<|=|\^|&|\|)'),

    # 6. Identifiers
    ('IDENTIFIER',  r'\b[a-zA-Z_\u00C0-\u024F][a-zA-Z0-9_\u00C0-\u024F!]*\b'),

    # 7. Operators (multi-char first, then single)
    ('OPERATOR',    r'>=|<=|==|!=|&&|\|\||->|=>|\.\.\.|\.\.|\^|\+|-|\*|/|%|=|>|<|!|&|\|'),

    # 8. Punctuation
    ('PUNCTUATION', r'[\(\),\[\]\{\};]'),

    # 9. Colon (standalone, after SYMBOL has taken :identifier forms)
    ('OPERATOR',    r':'),

    # 10. Whitespace
    ('SKIP',        r'[ \t\n\r]+'),

    # 11. Catch-all
    ('MISMATCH',    r'.'),
]

MASTER_REGEX = re.compile(
    '|'.join(f'(?P<{name}_{i}>{pattern})' for i, (name, pattern) in enumerate(TOKEN_RULES)),
    re.UNICODE,
)

# Map indexed group names back to logical token types
_GROUP_MAP = {f'{name}_{i}': name for i, (name, _) in enumerate(TOKEN_RULES)}


# ---------------------------------------------------------------------------
# String interpolation subdivision
# ---------------------------------------------------------------------------

def _subdivide_string(raw_value, line_num):
    """Break a raw Julia string token into sub-tokens for $-interpolation."""
    segments = []
    i = 1  # skip opening "
    end = len(raw_value) - 1  # skip closing "
    buf = []

    while i < end:
        ch = raw_value[i]
        if ch == '\\':
            buf.append(raw_value[i:i+2])
            i += 2
        elif ch == '$' and i + 1 < end:
            # flush literal so far
            if buf:
                segments.append(('STRING_PART', '"' + ''.join(buf) + '"', line_num))
                buf = []
            segments.append(('INTERP_START', '$', line_num))
            i += 1
            # grab identifier or parenthesised expression
            if i < end and raw_value[i] == '(':
                depth = 1
                i += 1
                expr = []
                while i < end and depth:
                    if raw_value[i] == '(':
                        depth += 1
                    elif raw_value[i] == ')':
                        depth -= 1
                    if depth:
                        expr.append(raw_value[i])
                    i += 1
                segments.append(('INTERP_EXPR', ''.join(expr), line_num))
            else:
                m = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', raw_value[i:])
                if m:
                    segments.append(('INTERP_IDENT', m.group(), line_num))
                    i += len(m.group())
        else:
            buf.append(ch)
            i += 1

    if buf:
        segments.append(('STRING_PART', '"' + ''.join(buf) + '"', line_num))

    # If no interpolation found, return as plain STRING
    if not any(t[0].startswith('INTERP') for t in segments):
        return [('STRING', raw_value, line_num)]

    # Wrap with STRING_START / STRING_END
    return [('STRING_START', '"', line_num)] + segments + [('STRING_END', '"', line_num)]


# ---------------------------------------------------------------------------
# Core tokenizer
# ---------------------------------------------------------------------------

def tokenize(code_text):
    """
    Scans Julia source text and returns:
        [(TOKEN_TYPE, VALUE, LINE_NUMBER, COLUMN), ...]

    Handles:
    - Precise line + column tracking
    - Nested block comments  #= ... =#
    - Julia symbol literals  :name
    - String $-interpolation
    - Resilient error recovery (MISMATCH → ERROR token, continues)
    """
    tokens = []
    errors = []
    line_num = 1
    line_start = 0

    pos = 0
    length = len(code_text)

    def current_col(abs_pos):
        return abs_pos - line_start + 1

    while pos < length:
        # ---- Nested block comments ----------------------------------------
        if code_text[pos:pos+2] == '#=':
            col = current_col(pos)
            depth = 1
            pos += 2
            while pos < length and depth > 0:
                if code_text[pos:pos+2] == '#=':
                    depth += 1
                    pos += 2
                elif code_text[pos:pos+2] == '=#':
                    depth -= 1
                    pos += 2
                else:
                    if code_text[pos] == '\n':
                        line_num += 1
                        line_start = pos + 1
                    pos += 1
            if depth != 0:
                errors.append(('ERROR', 'Unterminated block comment', line_num, col))
            # Block comments are discarded (not added to token list)
            continue

        # ---- Everything else via master regex --------------------------------
        m = MASTER_REGEX.match(code_text, pos)
        if not m:
            # Should never happen because MISMATCH catches everything
            errors.append(('ERROR', code_text[pos], line_num, current_col(pos)))
            pos += 1
            continue

        col = current_col(m.start())
        kind_raw = m.lastgroup
        kind = _GROUP_MAP[kind_raw]
        value = m.group(kind_raw)
        pos = m.end()

        if kind == 'SKIP':
            if '\n' in value:
                line_num += value.count('\n')
                line_start = m.start() + value.rfind('\n') + 1
            continue

        if kind == 'COMMENT':
            continue

        if kind == 'BLOCK_COMMENT_START':
            # Shouldn't reach here (handled above), but just in case
            continue

        if kind == 'MISMATCH':
            errors.append(('ERROR', value, line_num, col))
            tokens.append(('ERROR', value, line_num, col))
            continue

        if kind == 'STRING':
            sub = _subdivide_string(value, line_num)
            for st, sv, sl in sub:
                tokens.append((st, sv, sl, col))
            continue

        tokens.append((kind, value, line_num, col))

    return tokens, errors