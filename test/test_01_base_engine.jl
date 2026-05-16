# ---------------------------------------------------------
# Test File 1: Base Engine Features
# Tests: Keywords, INT, FLOAT, STRING, Operators, Delimiters
# ---------------------------------------------------------

function calculate_statistics(data_array, threshold)
    global total_sum = 0.0
    valid_count = 0
    
    for value in data_array
        if value >= threshold
            total_sum = total_sum + value
            valid_count = valid_count + 1
        elseif value == 0
            # Skip zero values
            total_sum = total_sum + 0
        else
            total_sum = total_sum - 1.5
        end
    end
    
    while valid_count < 10
        valid_count = valid_count + 1
    end
    
    result_string = "Calculation finished"
    return total_sum
end

my_data = [10, 20.5, 30, 0, 5.5]
my_dict = {"status" : "active"}