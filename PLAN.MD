# Julia Lexer Project Expansion Plan

This document outlines the architectural plan for our **Julia Lexer (Lexical Analyzer)**. It details what has already been achieved by our base engine, identifies critical engineering fixes, and maps out the advanced features required to elevate this from a simple script to an enterprise-grade academic compiler front-end.

---

## 🛠 Current Progress (What is Already Done)

Our current lexer engine successfully establishes a robust foundation using a deterministic **Master Regular Expression Architecture** mapped to named capture groups. 

### 1. Implemented Token Rules
The lexer accurately scans, categorizes, and produces tuples for the following standard structural elements:
* **Comments:** Single-line tracking using `#.*`.
* **Keywords:** Identification of core Julia control structures (`function`, `end`, `if`, `elseif`, `else`, `while`, `for`, `in`, `return`, `global`).
* **Literals:** Whole integers (`INT`), double-precision floating-point numbers (`FLOAT`), and basic string literals wrapped in double quotes (`STRING`).
* **Identifiers:** Alphanumeric variable and function names conforming to `[a-zA-Z_][a-zA-Z0-9_]*`.
* **Operators:** Mathematical, relational, and assignment operators (`>=`, `<=`, `==`, `!=`, `+`, `-`, `*`, `/`, `=`, `:`, `>`, `<`).
* **Punctuation & Delimiters:** Structural characters including `( )`, `[ ]`, `{ }`, and `,`.

### 2. Operational Pipelines
* **Master Regex Matching:** Leverages Python’s internal `re.finditer()` engine to evaluate rules efficiently in a single scanning pass.
* **File Processor (`main.py`):** An automated pipeline that looks up specified source paths (`test/*.jl`), feeds them to the engine, handles exceptions cleanly, and logs readable token matrices to `output/*_tokens.txt`.

---

## 🚀 Future Roadmap & To-Do List

To transition this codebase into a comprehensive, robust scanner for a *Principles of Programming Languages* project, the team will implement the following extensions over the next week.

### 🟥 Phase 1: Critical Bug Fixes & Lexer Correctness
- [ ] **Fix Column Tracking Defect:** * *Problem:* The current column math (`match.start() - line_start + 1`) fails because `line_start` is never updated when newlines are processed inside skipped whitespace blocks.
  * *Solution:* Modify the `SKIP` category logic to record the exact position of the last observed `
` character (`line_start = match.start() + value.rfind('
') + 1`) to reset the column offset precisely.
- [ ] **Address Word-Boundary Glitches on Operators:** Ensure operators or symbol combinations do not blend accidentally with word boundary tokens (`\b`), establishing strict priority sequencing.

### 🟨 Phase 2: Julia-Specific Syntax Depth
- [ ] **Nested Block Comments Handling (`#= ... =#`):**
  * *Challenge:* Block comments in Julia can be deep-nested inside other block comments. Because nested structures represent a Context-Free Grammar (CFG) rather than a Regular Language, standard RegEx patterns cannot parse them.
  * *Solution:* Implement an explicit lexical state tracking mechanism. When encountering `#=`, increment a nesting counter; when meeting `=#`, decrement it. Do not return to normal lexing until the counter drops back to zero.
- [ ] **Julia Symbol Literals:**
  * *Requirement:* Support symbols like `:my_var` or `:+=` without breaking the standard `:` operator or punctuation definitions.
- [ ] **String Interpolation Scanning:**
  * *Requirement:* Detect expressions inside strings (e.g., `"Value: $x"`). Subdivide strings into multi-part token structures: `STRING_START`, `INTERPOLATION_START`, `IDENTIFIER`, and `STRING_END`.

### 🟩 Phase 3: Compiler Architecture & Data Structures
- [ ] **Incorporate a Comprehensive Symbol Table:**
  * *Objective:* Shift from flat token generation to a professional compiler design. Build a dedicated `SymbolTable` class.
  * *Functionality:* Capture identifiers, track their line/column scope definitions, cross-reference multiple appearances, and record inferred attributes (e.g., variable vs. function target via lookahead).
  * *Output:* Generate an independent `output/symbol_table.txt` tracking table.
- [ ] **Resilient Error Recovery System:**
  * *Current State:* The compiler crashes immediately on the first invalid character via `SyntaxError`.
  * *New State:* Catch `MISMATCH` instances, log them as explicit `ERROR` tokens, report the faulty line/column, skip the illegal character, and seamlessly continue lexing to catch all syntax errors in a single execution.

### 🟦 Phase 4: Developer UX & Testing Infrastructure
- [ ] **Robust Command Line Interface (CLI):** * Refactor `main.py` using Python's `argparse` package to accept custom user flags (e.g., `--input file.jl --output out.txt --verbose`).
- [ ] **Automated Regression Suite (Golden Master Testing):**
  * Construct a test verification routine that automatically diffs newly generated token logs against hand-verified "Golden Master" baselines to instantly verify that refactoring hasn't broken working components.

---