# ---------------------------------------------------------
# Test File 5: Error Recovery
# Tests: Illegal characters, uninterrupted scanning
# ---------------------------------------------------------

function faulty_code_test()
    valid_number = 100
    
    # Intentionally inserting an illegal character '@' 
    # The lexer should flag '@' as an ERROR but successfully lex 'invalid_var' and '=' and '200'
    invalid_var@ = 200 
    
    # Intentionally inserting an unsupported backtick '`' or '?'
    `bad_command` = 50
    result = valid_number ? 5 
    
    return valid_number
end