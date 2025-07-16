#recursion is a function that calls itself

#example 1: Factorial is the product of all positive integers less than or equal to n.
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))

#example 2: Fibonacci is a sequence of numbers where each number is the sum of the two preceding ones, starting from 0 and 1.
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))

#example 3: Palindrome is a word that reads the same forward and backward.
def palindrome(word):
    if len(word) <= 1: #the base case is when the word is 1 or less than 1
        return "palindrome"
    else:
        if word[0] == word[-1]:
            palindrome(word[1:-1])
            return "palindrome"
        else:
            print("not a palindrome")

print(palindrome("madam"))
print(palindrome("racecar"))

#example 4: Rabbit population growth 
#see image in the folder

def rabbit_population(n):
    if n == 0:
        return 1
    else:
        return rabbit_population(n-1) + rabbit_population(n-2)

print(rabbit_population(5))