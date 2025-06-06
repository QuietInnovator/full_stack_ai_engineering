import utils

# get user input
a = int(input("Enter a number: "))
b = int(input("Enter another number: "))

# call the functions
result = utils.add(a, b)
print(f"The result of adding {a} and {b} is {result}")

result = utils.subtract(a, b)
print(f"The result of subtracting {a} and {b} is {result}")

result = utils.multiply(a, b)
print(f"The result of multiplying {a} and {b} is {result}")

result = utils.divide(a, b)
print(f"The result of dividing {a} and {b} is {result}")