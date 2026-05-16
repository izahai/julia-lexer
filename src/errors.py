"""
errors.py
---------
Structured error reporting for the Julia lexer.
Errors are collected throughout a run rather than crashing on first hit.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class LexerError:
    character: str
    line: int
    col: int
    message: str = ''

    def __str__(self):
        desc = self.message or f"Illegal character {self.character!r}"
        return f"  [ERROR] {desc} at line {self.line}, column {self.col}"


class ErrorReporter:
    def __init__(self):
        self._errors: List[LexerError] = []

    def add(self, character: str, line: int, col: int, message: str = ''):
        self._errors.append(LexerError(character, line, col, message))

    def from_token_list(self, error_tuples):
        """Accept (kind, value, line, col) tuples where kind == 'ERROR'."""
        for tup in error_tuples:
            _, value, line, col = tup
            self.add(value, line, col)

    @property
    def has_errors(self):
        return bool(self._errors)

    @property
    def count(self):
        return len(self._errors)

    def report(self) -> str:
        if not self._errors:
            return "No lexer errors detected."
        lines = [f"=== {self.count} LEXER ERROR(S) DETECTED ==="]
        for err in self._errors:
            lines.append(str(err))
        return '\n'.join(lines)

    def write(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.report())
            f.write('\n')