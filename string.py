#string
""" s = "hello"
str = 'world'"""
# string = """hello"""

#space sequence character
""" string = "hello\nworld"
print(string) """

#basic string operations
#concatenation
""" str1 = "hello"
str2 = "world"
str3 = str1 + str2
print(str3) """

#calculate length of string
""" string = "hello" + " " + "world"
print(len(string)) """

#accessing string characters
string = "hello"
print(string[0])

#slicing string
#str[starting_index:ending_index] #last index is not included
""" string = "hello world" #negative index is like d= -1, l= -2, o= -3, etc
print(string[0:5])
print(string[6:11])
print(string[0:11])
print(string[0:])
print(string[:5])
print(string[:])
print(string[0:11:2])
print(string[::2])
print(string[::-1]) """

#string functions
#len()
""" string = "hello world"
print(len(string)) """
#count()
""" string = "hello world"
print(string.count("l")) """
#capitalize()
""" string = "hello world"
print(string.capitalize()) """
#title()
""" string = "hello world"
print(string.title()) """
#swapcase()
""" string = "hello world"
print(string.swapcase()) """
#replace()
""" string = "hello world"
print(string.replace("hello", "world")) """
#split()
""" string = "hello world"
print(string.split()) """
#join()
""" string = "hello world"
print(string.join("world")) """
#find()
""" string = "hello world"
print(string.find("world")) """
#index()
""" string = "hello world"
print(string.index("world")) """
#isalpha()
""" string = "hello world"
print(string.isalpha()) """
#isdigit()
""" string = "hello world"
print(string.isdigit()) """
#isendwith()
""" string = "hello world"
print(string.endswith("world")) """
#isstartwith()
""" string = "hello world"
print(string.startswith("hello")) """
#isupper()
""" string = "hello world"
print(string.isupper()) """
#islower()
""" string = "hello world"
print(string.islower()) """
#isspace()
""" string = "hello world"
print(string.isspace()) """
#isalnum()
""" string = "hello world"
print(string.isalnum()) """
#isdecimal()
""" string = "hello world"
print(string.isdecimal()) """

#string methods
""" string = "hello world"
print(string.upper())
print(string.lower())
print(string.capitalize())
print(string.title())
print(string.swapcase())
print(string.replace("hello", "world"))"""

#conditional statements
""" if 5 > 3:
    print("5 is greater than 3")
else:
    print("5 is not greater than 3") """