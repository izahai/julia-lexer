## Repository Structure
* `main.py`: Refactored CLI driver script using `argparse` to support flexible `--input`, `--output`, and `--verbose` configurations.
* `src/lexer.py`: The core tokenization engine utilizing a Master Regular Expression Architecture paired with custom state machines for complex contexts.
* `src/symbol_table.py`: Dedicated tracking system that maps, registers, and scopes identifiers and their metadata across execution.
* `test/`: Folder containing regression suite files (`.jl`) utilized for "Golden Master" differential testing.
* `output/`: Folder containing generated token tables (`_tokens.txt`) and structural maps (`symbol_table.txt`).

## Advanced Capabilities (Newly Added)
* **Nested Block Comments:** State-tracking parser layer that accurately counts and bypasses arbitrarily deep nested `#= ... =#` blocks.
* **Julia Symbol Literals:** Disambiguates `:` range/operators to cleanly extract symbol identifiers (e.g., `:initializing`, `:+=`).
* **String Interpolation State-Machine:** Dynamically slices string literals into sub-tokens (`STRING_START`, `INTERP_START`, `INTERP_IDENT`, `STRING_END`) upon encountering `$`.
* **Integrated Symbol Table:** Tracks, aggregates, and exports all identifiers to a decoupled cross-referenced database (`output/symbol_table.txt`) for later downstream phases.
* **Panic-Mode Error Recovery:** Replaced crashing runtime halts with resilient continuous scanning; captures multiple isolated `ERROR` tokens per pass without interrupting source analysis.

## How to Run

1. Open your terminal in the root directory (`julia-lexer/`).
2. Run the refactored CLI with optional flags:
   ```bash
   python3 main.py --input test/test_04_symbols_and_interpolation.jl --verbose