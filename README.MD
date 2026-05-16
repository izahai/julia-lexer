# Julia Lexical Analyzer (Lexer)

A lightweight lexical analyzer for the Julia programming language built in Python. This project was developed for the *Principles of Programming Languages* course.

## Group Information
* **Language Assigned:** Julia
* **Group Members:** 

## Repository Structure
* `main.py`: The main driver script that coordinates reading, tokenizing, and exporting.
* `lexer.py`: The tokenization engine utilizing regular expressions (`re` module) mapped to Julia grammar.
* `test/`: Folder containing valid Julia scripts (`.jl`) used to evaluate the lexer.
* `output/`: Folder containing the resulting token sheets (`_tokens.txt`).

## Supported Tokens
The lexer categorizes Julia components into the following token types:
* **KEYWORDS:** `function`, `end`, `if`, `elseif`, `else`, `while`, `for`, `in`, `return`, `global`
* **LITERALS:** Integers, Floats, and Strings
* **IDENTIFIERS:** Variable and function names
* **OPERATORS:** Arithmetic and comparison symbols (`+`, `-`, `*`, `/`, `=`, `==`, `>=`, `<=`, etc.)
* **PUNCTUATION:** Parentheses, brackets, and commas `() [] {} ,`

*Note: Code comments (`# ...`) and whitespace are automatically handled and skipped.*

## How to Run

1. Open your terminal in the root directory (`julia-lexer/`).
2. Execute the controller script using Python 3:
   ```bash
   python3 main.py
   ```
3. Check the (`output/`) directory to view the generated token tables.
---