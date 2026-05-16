# ---------------------------------------------------------
# Test File 2: Column Tracking & Word Boundaries
# Tests: Erratic spacing, tabs, newlines, operator boundaries
# ---------------------------------------------------------

function spacing_test()
    x=10
    y   =   20
    
    # The next line has heavy indentation to test column offsets
                            z = x + y

    # Testing word boundaries on operators so they don't blend
    a=b+c
    if x>=y
        return x==y!=z
    end
    
    return z
end