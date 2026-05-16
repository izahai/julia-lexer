# ---------------------------------------------------------
# Test File 4: Symbols and String Interpolation
# Tests: :symbol, :+=, "String $var"
# ---------------------------------------------------------

function string_and_symbols()
    # Symbol Literals
    state = :initializing
    math_op = :+=
    node_name = :ast_node_1
    
    # Standard String vs Interpolated String
    user = "Compiler_Dev"
    errors = 0
    
    # Lexer should subdivide this into: 
    # STRING_START, INTERPOLATION_START, IDENTIFIER (user), STRING_TEXT, INTERPOLATION_START, IDENTIFIER (errors), STRING_END
    log_message = "User $user finished with $errors errors."

    println(math_op)
    println(state)
    println(node_name)
    println(log_message)
    
    return state
end

string_and_symbols()