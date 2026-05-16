# ---------------------------------------------------------
# Test File 3: Nested Block Comments
# Tests: #= ... =# and deep nesting structures
# ---------------------------------------------------------

#= 
This is a standard multi-line block comment.
The lexer should ignore everything in here.
x = 100 
=#

function comment_nesting_test()
    #= 
    Outer block comment begins.
    Level 1 nesting.
        #= 
        Inner block comment begins.
        Level 2 nesting.
        The lexer state tracker should hit 2, then drop to 1 here:
        =#
    Back to Level 1 nesting.
    =#
    
    active_variable = 500
    return active_variable
end