# Testing conditional statements and loops
score = 85

if score >= 90
    status = "Excellent"
elseif score >= 75
    status = "Pass"
else
    status = "Fail"
end

println("Student Status: ", status)

# A simple while loop countdown
count = 3
while count > 0
    println("Countdown: ", count)
    global count = count - 1  # Note: 'global' is needed in Julia scripts inside loops
end