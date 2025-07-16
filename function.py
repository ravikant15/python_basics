#function is a block of code that performs a specific task

#def function_name(arguments):
#    instructions
#def is used to define a function
#function_name is the name of the function
#arguments are the parameters passed to the function
#return is used to return a value from the function
#return is optional
#if return is not used, the function will return None
#if return is used, the function will return the value
#function works on two principles
#1. Abstraction
#2. Decomposition

#function definition

def adda(a,b):
    return a+b

#function call
print(adda(1,2))

#function with default arguments
def sadnk(a,b=10):
    return a+b

#function with variable length arguments
def add_numbers(*args):
    return sum(args)

#function with keyword arguments
def add_numbersa(**kwargs):
    return sum(kwargs.values())

#function with default and keyword arguments
def add(a,b=10,**kwargs):
    return a+b+sum(kwargs.values())

def is_even(a):
    if a %2 == 0:
        return "Even"
    else:
        return "Odd"
        
x = is_even(4)
print(x)


#arguments 
#1. Default arguments -> default arguments are passed to the function if no value is provided for the argument
def add_numbers_default(a,b=10):
    return a+b

print(add_numbers_default(1,2))

#1. Positional arguments -> positional arguments are passed to the function in the order they are defined
def add_numbers_positional(a,b):
    return a+b

print(add_numbers_positional(1,2))

#2. Keyword arguments -> keyword arguments are passed to the function with the key and value pair as they donot rely on the order of the arguments
def add_numbers_keyword(a,b):
    return a+b

print(add_numbers_keyword(a=1,b=2))

#3. Arbitrary arguments -> arbitrary arguments are passed to the function as a tuple
def add_numbers_arbitrary(*args):
    return sum(args)

print(add_numbers_arbitrary(1,2,3,4,5))

#4. Variable length arguments -> variable length arguments are passed to the function as a tuple
def add_numbers_variable(*args):
    return sum(args)
    
print(add_numbers_variable(1,2,3,4,5))

#5. Arbitrary keyword arguments -> arbitrary keyword arguments are passed to the function as a dictionary
def add_numbers_arbitrary_keyword(**kwargs):
    return sum(kwargs.values())

print(add_numbers_arbitrary_keyword(a=1,b=2,c=3,d=4,e=5))