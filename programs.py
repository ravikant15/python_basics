#float division means division of two integers will give float
# A,B = 1,2
# print(A/B)

#integer division with float and integer will give float same as floor value(rounding down)
# A,B,C = 1,2,3
# print(A/B,A//B)

#remainder is negative if the denominator is negative
# A,B = 1,-2
# print(A%B)

#power operator
# A,B = 2,3
# print(A**B)

#floor division
""" A,B = 1,2
floor_division = A//B
print(floor_division) """

#input in python
"""name = input("Enter your name: ")
age_int = int(input("Enter your age: "))
height_float = float(input("Enter your height: "))
print(name,age_int,height_float) """

#type casting
""" A = 1
B = 2.0
C = A+B
print(C) """

#conditional statements
#A = 5 & G = M
#A = 2 & G = F

"""A = int(input("A: "))
G = input("M/F: ")
if((A == 1 or A == 2) and G == "M"):
    print("You are a male and fee is 100")
elif((A == 3 or A == 4) and G == "F"):
    print("You are a female and fee is 200")
elif(A == 5 or A == 6):
    print("fee is 300")
else:
    print("Invalid input")"""


#<var> = <value1> if <condition> else <value2>
""" single_line_if_else = "You are a male and fee is 100" if A == 1 or A == 2 and G == "M" else "You are a female and fee is 200" if A == 3 or A == 4 and G == "F" else "fee is 300" if A == 5 or A == 6 else "Invalid input" """

#<str1> if <condition> else <str2>
""" food = input("Enter your food: ")
print("sweet") if(food == 'mango') else print("sour") if(food == 'orange') else print("salty") if(food == 'banana') else print("Invalid input") """

#assign variable value based on condition
#<var> = (false_val, true_val) [<condition>]
""" a = input("Enter a: ")
vote = ("yes","no") [a >= '18']
print(vote) """

#nested if else
""" A = int(input("Enter A: "))
if(A > 0):
    if(A > 10):
        print("A is greater than 10")
    else:
        print("A is less than 10") """

#nested if else with single line
""" A = int(input("Enter A: "))
print("A is greater than 10") if(A > 0) and (A > 10) else print("A is less than 10") """

#nested if else with single line and if else
""" A = int(input("Enter A: "))
print("A is greater than 10") if(A > 0) and (A > 10) else print("A is less than 10") """

#operators means a symbol which performs an operation between two operands
#type 1: arithmetic operators
""" A,B = 1,2
print(A+B)
print(A-B)
print(A*B)
print(A/B)
print(A%B)
print(A**B)
print(A//B) """

#type 2: relational / comparison operators
""" A,B = 1,2
print(A==B)
print(A!=B)
print(A>B)
print(A<B)
print(A>=B)
print(A<=B) """

#type 3: logical operators
""" A,B = True,False
print(A and B)
print(A or B)
print(not A) """

#type 4: bitwise operators
""" A,B = 1,2
print(A&B)
print(A|B)
print(A^B)
"""

#type 5: membership operators
""" A = "hello"
B = "h"
print(B in A)
print(B not in A) """

#type 6: identity operators
""" A,B = 1,2
print(A is B)
print(A is not B) """

#type 7: assignment operators
""" A,B = 1,2
print(A+=B)
print(A-=B)
print(A*=B)
print(A/=B)
print(A%=B)
print(A**=B)
print(A//=B) """
