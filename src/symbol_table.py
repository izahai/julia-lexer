"""
symbol_table.py
---------------
Tracks every identifier seen during lexing: where it was first defined,
all subsequent references, and any inferred role (variable vs function).
"""

from collections import defaultdict


class SymbolEntry:
    def __init__(self, name, line, col):
        self.name = name
        self.first_seen = (line, col)
        self.references = []   # list of (line, col)
        self.role = 'variable' # 'variable' | 'function' | 'unknown'

    def add_reference(self, line, col):
        self.references.append((line, col))

    def __repr__(self):
        return (f"SymbolEntry(name={self.name!r}, role={self.role}, "
                f"first={self.first_seen}, refs={len(self.references)})")


class SymbolTable:
    def __init__(self):
        self._table: dict[str, SymbolEntry] = {}

    # ------------------------------------------------------------------
    def record(self, name: str, line: int, col: int, role: str = 'variable'):
        if name not in self._table:
            entry = SymbolEntry(name, line, col)
            entry.role = role
            self._table[name] = entry
        else:
            entry = self._table[name]
            entry.add_reference(line, col)
            # Upgrade role: if we discover it's a function, lock that in
            if role == 'function':
                entry.role = 'function'

    def get(self, name: str) -> SymbolEntry | None:
        return self._table.get(name)

    def all_entries(self):
        return sorted(self._table.values(), key=lambda e: e.first_seen)

    # ------------------------------------------------------------------
    def build_from_tokens(self, tokens):
        """
        Walk the token list produced by lexer.tokenize() and populate the
        symbol table.  Uses a one-token lookahead to detect function names:
          KEYWORD('function') → IDENTIFIER('foo')  ⇒  foo is a function
        """
        for i, tok in enumerate(tokens):
            kind = tok[0]
            value = tok[1]
            line = tok[2]
            col = tok[3]

            if kind == 'IDENTIFIER':
                # Lookahead: was previous non-whitespace token `function`?
                role = 'variable'
                if i > 0:
                    prev = tokens[i - 1]
                    if prev[0] == 'KEYWORD' and prev[1] == 'function':
                        role = 'function'
                self.record(value, line, col, role)

    # ------------------------------------------------------------------
    def format_table(self) -> str:
        lines = []
        header = f"{'SYMBOL':<20} | {'ROLE':<10} | {'FIRST LINE':<11} | {'FIRST COL':<10} | REFERENCES"
        lines.append(header)
        lines.append('-' * len(header))
        for entry in self.all_entries():
            refs = ', '.join(f"L{l}:C{c}" for l, c in entry.references) or '—'
            lines.append(
                f"{entry.name:<20} | {entry.role:<10} | "
                f"L{entry.first_seen[0]:<10} | C{entry.first_seen[1]:<9} | {refs}"
            )
        return '\n'.join(lines)

    def write(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=== JULIA LEXER – SYMBOL TABLE ===\n\n")
            f.write(self.format_table())
            f.write('\n')