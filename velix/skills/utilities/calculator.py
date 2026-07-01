import math

"""
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
print("5. Exponentiation")
print("6. Square Root")

"""

def add(a,b):
    print(f"Answer is : {a + b}")

def subtract(a, b):
    print(f"Answer is {a - b}")

def multiply(a, b):
    print(f"Answer is : {a*b}")

def divide(a, b):
    print(f"{a/b }")

def exponent(a:float,b:float):
    c = math.pow(a,b)
    print(f"The exponent is {c}")

def sq_root(a):
    print(f"The square-root of {a} is {math.sqrt(a):.2f}")
    