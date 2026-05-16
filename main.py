"""
main.py
-------
Julia Lexer – command-line entry point.

Usage examples
--------------
# Process all default test files:
    python main.py

# Process a single custom file with verbose output:
    python main.py --input path/to/file.jl --output path/to/out.txt --verbose

# Run the automated regression / golden-master test suite:
    python main.py --test

# Regenerate golden-master baselines from current output:
    python main.py --update-baselines
"""

import argparse
import difflib
import os
import sys

from src.lexer import tokenize
from src.symbol_table import SymbolTable
from src.errors import ErrorReporter


# ---------------------------------------------------------------------------
# Default file mappings
# ---------------------------------------------------------------------------
DEFAULT_MAPPINGS = [
    ("test/test_01_base_engine.jl",             "output/test1_tokens.txt"),
    ("test/test_02_whitespace_and_columns.jl", "output/test2_tokens.txt"),
    ("test/test_03_advanced_comments.jl",       "output/test3_tokens.txt"),
    ("test/test_04_symbols_and_interpolation.jl", "output/test4_tokens.txt"),
    ("test/test_05_error_recovery.jl",          "output/test5_tokens.txt"),
    ("test/test_06_golden_master.jl",           "output/test6_tokens.txt"),
]

BASELINE_DIR = "test/baselines"
SYMBOL_TABLE_OUT = "output/symbol_table.txt"
ERRORS_OUT = "output/lexer_errors.txt"


# ---------------------------------------------------------------------------
# Token formatting helpers
# ---------------------------------------------------------------------------

def _format_tokens(tokens: list) -> str:
    header = f"{'TOKEN TYPE':<20} | {'VALUE':<25} | {'LINE':<6} | COL\n"
    separator = "-" * 62 + "\n"
    rows = []
    for tok in tokens:
        kind, value, line, col = tok
        clean = value.replace('\n', '\\n').replace('\r', '\\r')
        rows.append(f"{kind:<20} | {clean:<25} | {line:<6} | {col}")
    return header + separator + '\n'.join(rows) + '\n'


# ---------------------------------------------------------------------------
# Single-file processor
# ---------------------------------------------------------------------------

def process_file(input_path: str, output_path: str, verbose: bool = False,
                 global_symtable: SymbolTable = None,
                 global_errors: ErrorReporter = None):
    if verbose:
        print(f"\nProcessing: {input_path}")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {input_path}")
        return None

    tokens, raw_errors = tokenize(code)

    # ---- Symbol table -------------------------------------------------------
    local_sym = SymbolTable()
    local_sym.build_from_tokens(tokens)
    if global_symtable is not None:
        # Merge into the global table
        for entry in local_sym.all_entries():
            global_symtable.record(entry.name, *entry.first_seen, role=entry.role)
            for ref in entry.references:
                global_symtable.record(entry.name, *ref)

    # ---- Error reporter -----------------------------------------------------
    if global_errors is not None and raw_errors:
        for tup in raw_errors:
            _, value, line, col = tup
            global_errors.add(value, line, col)

    # ---- Write token output -------------------------------------------------
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    formatted = _format_tokens(tokens)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Source: {input_path}\n")
        f.write(formatted)

    error_count = len(raw_errors)
    if verbose:
        print(f"  Tokens: {len(tokens)}  |  Errors: {error_count}")
        if error_count:
            for _, val, ln, col in raw_errors:
                print(f"    [LEXER ERROR] Illegal char {val!r} at L{ln}:C{col}")
        print(f"  Output written → {output_path}")
        print(f"  Symbols found:  {len(local_sym.all_entries())}")

    return formatted


# ---------------------------------------------------------------------------
# Regression / golden-master testing
# ---------------------------------------------------------------------------

def run_tests(verbose: bool = False):
    print("\n=== RUNNING REGRESSION SUITE ===\n")
    os.makedirs(BASELINE_DIR, exist_ok=True)
    passed = failed = skipped = 0

    for input_path, output_path in DEFAULT_MAPPINGS:
        baseline_path = os.path.join(BASELINE_DIR, os.path.basename(output_path))

        if not os.path.exists(input_path):
            print(f"  [SKIP] {input_path} not found")
            skipped += 1
            continue

        if not os.path.exists(baseline_path):
            print(f"  [SKIP] No baseline for {os.path.basename(output_path)} — run --update-baselines first")
            skipped += 1
            continue

        current = process_file(input_path, output_path, verbose=False)
        with open(baseline_path, 'r', encoding='utf-8') as f:
            baseline = f.read()

        if current == baseline:
            print(f"  [PASS] {os.path.basename(input_path)}")
            passed += 1
        else:
            print(f"  [FAIL] {os.path.basename(input_path)}")
            diff = difflib.unified_diff(
                baseline.splitlines(keepends=True),
                current.splitlines(keepends=True),
                fromfile='baseline',
                tofile='current',
                n=3,
            )
            print(''.join(list(diff)[:40]))   # show first 40 diff lines
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    return failed == 0


def update_baselines(verbose: bool = False):
    print("\n=== UPDATING GOLDEN-MASTER BASELINES ===\n")
    os.makedirs(BASELINE_DIR, exist_ok=True)

    for input_path, output_path in DEFAULT_MAPPINGS:
        if not os.path.exists(input_path):
            print(f"  [SKIP] {input_path} not found")
            continue
        content = process_file(input_path, output_path, verbose=verbose)
        if content is None:
            continue
        baseline_path = os.path.join(BASELINE_DIR, os.path.basename(output_path))
        with open(baseline_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [SAVED] {baseline_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog='julia-lexer',
        description='Julia Lexical Analyzer — tokenizes .jl source files',
    )
    parser.add_argument('--input',  '-i', metavar='FILE',
                        help='Single input .jl file to tokenize')
    parser.add_argument('--output', '-o', metavar='FILE',
                        help='Output token file (used with --input)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print detailed progress to stdout')
    parser.add_argument('--test', action='store_true',
                        help='Run regression suite against golden-master baselines')
    parser.add_argument('--update-baselines', action='store_true',
                        help='Regenerate golden-master baselines from current output')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # ---- Regression mode ----------------------------------------------------
    if args.test:
        ok = run_tests(verbose=args.verbose)
        sys.exit(0 if ok else 1)

    if args.update_baselines:
        update_baselines(verbose=args.verbose)
        sys.exit(0)

    # ---- Single-file mode ---------------------------------------------------
    if args.input:
        output = args.output or args.input.replace('.jl', '_tokens.txt')
        sym = SymbolTable()
        err = ErrorReporter()
        process_file(args.input, output, verbose=True, global_symtable=sym, global_errors=err)
        sym.write(SYMBOL_TABLE_OUT)
        if err.has_errors:
            err.write(ERRORS_OUT)
            print(err.report())
        sys.exit(0)

    # ---- Default batch mode -------------------------------------------------
    print("=== JULIA LEXER PROCESSOR ===\n")
    sym = SymbolTable()
    err = ErrorReporter()

    for input_path, output_path in DEFAULT_MAPPINGS:
        if os.path.exists(input_path):
            process_file(input_path, output_path,
                         verbose=args.verbose,
                         global_symtable=sym,
                         global_errors=err)
            status = "OK"
        else:
            status = "SKIPPED (file not found)"
        print(f"  {input_path:<35} → {output_path}  [{status}]")

    # Write aggregate symbol table
    os.makedirs('output', exist_ok=True)
    sym.write(SYMBOL_TABLE_OUT)
    print(f"\nSymbol table → {SYMBOL_TABLE_OUT}")

    # Write error log if any errors occurred
    if err.has_errors:
        err.write(ERRORS_OUT)
        print(f"Errors log   → {ERRORS_OUT}  ({err.count} error(s))")
    else:
        print("No lexer errors detected.")

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()