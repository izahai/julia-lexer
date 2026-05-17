# Julia Lexical Analyzer (Lexer)

A lightweight lexical analyzer for the Julia programming language built in Python. This project was developed for the *Principles of Programming Languages* course.

---

## Repository Structure
- `main.py` — Refactored CLI driver script using `argparse` with configurable `--input`, `--output`, and `--verbose` options.
- `src/lexer.py` — Core tokenization engine built on a Master Regular Expression Architecture with supplementary state machines for complex lexical contexts.
- `src/symbol_table.py` — Tracks and aggregates every identifier encountered during the lexing phase, mapping each unique name to its definition, role, and usage history.
- `src/errors.py` — Structured lexer error handling and reporting system with aggregated diagnostics and file export support.
- `test/` — Collection of Julia test programs (`.jl`) used for regression and Golden Master testing.
- `output/` — Generated token reports (`_tokens.txt`) and symbol table exports (`symbol_table.txt`).

---

## Supported Tokens
The lexer recognizes and categorizes the following Julia language components:

### Keywords
`function`, `end`, `if`, `elseif`, `else`, `while`, `for`, `in`, `return`, `global`

### Literals
- Integers
- Floating-point numbers
- Strings
- Julia Symbol Literals (e.g. `:init`, `:+=`)

### Identifiers
- Variable names
- Function names

### Operators
Arithmetic and comparison operators including:
`+`, `-`, `*`, `/`, `=`, `==`, `>=`, `<=`, `:`, and others.

### Punctuation
`() [] {} ,`

### Ignored Elements
- Whitespace
- Single-line comments (`# ...`)
- Nested block comments (`#= ... =#`)

---

## Advanced Capabilities
- **Nested Block Comment Parsing**  
  Supports arbitrarily deep nested Julia block comments using state-based tracking.

- **String Interpolation Handling**  
  Detects and tokenizes interpolated strings into structured sub-tokens such as:
  `STRING_START`, `INTERP_START`, `INTERP_IDENT`, and `STRING_END`.

- **Integrated Symbol Table**  
  Tracks identifiers and exports cross-referenced symbol metadata to:
  `output/symbol_table.txt`.

- **Panic-Mode Error Recovery**  
  Continues lexical analysis after malformed input by emitting isolated `ERROR` tokens instead of terminating execution.

- **Flexible CLI Execution**  
  Provides configurable input/output handling and optional verbose token tracing.

---

## How to Run

1. Open a terminal in the project root directory:
   ```bash
   cd julia-lexer
   ```
2. Run the lexer:
   ```bash
   python3 main.py
   ```
3. Run with custom options:
   ```bash
   python3 main.py --input test/test_04_symbols_and_interpolation.jl --verbose
   ```
4. View generated outputs in:
   - output/*_tokens.txt
   - output/symbol_table.txt
   - output/lexer_errors.txt (if any)