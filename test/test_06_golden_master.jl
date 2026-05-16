#= 
===========================================================
Golden Master Test Suite
This file contains every lexical feature supported by the
Julia Lexer Project. Use this for regression testing.
===========================================================
=#

global environment = :production

function process_telemetry(data_stream, multiplier)
    # Validate the input
    if data_stream == 0
        return "Error: $data_stream is empty"
    end
    
    # Initialize variables for Symbol Table tracking
    # (Notice multiple assignments to 'total' to test symbol scoping/references)
    total = 0.0 
    pointer = 1
    
    #= 
       Begin data processing loop
       #= nested warning: complex math ahead =#
    =#
    for val in data_stream
        if val >= 0
            adjusted_val = val * multiplier
            total = total + adjusted_val
        else
            total = total - val
        end
    end
    
    # Let's test some operators and symbols
    status_code = :success
    complex_op = :*=
    
    # The following line contains an intentional error for the recovery system:
    final_output^ = total
    
    report = "Telemetry processed. Status: $status_code. Final sum: $total."
    return report
end

# Execution
sample_data = [15.5, 20.0, 3.14, 0, 42.0]
process_telemetry(sample_data, 2.5)