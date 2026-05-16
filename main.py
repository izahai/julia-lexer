import os
from lexer import tokenize

def process_test_file(input_path, output_path):
    print(f"Processing: {input_path} -> {output_path}")
    
    try:
        # 1. Read the raw Julia test file
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        # 2. Run the code through our lexer engine
        tokens = tokenize(code)
        
        # 3. Format and save the results to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{'TOKEN TYPE':<15} | {'VALUE':<20} | LINE\n")
            f.write("-" * 46 + "\n")
            for kind, value, line in tokens:
                # Truncate newlines in values just in case
                clean_value = value.replace('\n', '\\n')
                f.write(f"{kind:<15} | {clean_value:<20} | Line {line}\n")
                
        print("  [SUCCESS] Tokens successfully generated.")
        
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {input_path}")
    except SyntaxError as e:
        print(f"  [LEXER CRASHED] {e}")

def main():
    # Define our files exactly mapping to your repo layout
    file_mappings = [
        ("test/test1_basic.jl", "output/test1_tokens.txt"),
        ("test/test2_loop.jl", "output/test2_tokens.txt"),
        ("test/test3_func.jl", "output/test3_func_tokens.txt") # Your directory had test3_func.jl
    ]
    
    print("=== STARTING JULIA LEXER PROCESSOR ===\n")
    
    for input_file, output_file in file_mappings:
        # Check if input file exists before running
        if os.path.exists(input_file):
            process_test_file(input_file, output_file)
        else:
            print(f"Skipping {input_file} (File doesn't exist yet)")
            
    print("\n=== LEXING COMPLETE ===")

if __name__ == "__main__":
    main()