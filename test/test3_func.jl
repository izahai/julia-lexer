# Testing Julia functions and for-loops
function calculate_sum(limit)
    total = 0
    for i in 1:limit
        total = total + i
    end
    return total
end

# Call the function and print the output
final_score = calculate_sum(10)
println("The sum from 1 to 10 is: ", final_score)