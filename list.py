# list is a collection of items
#it can store different types of data like int, float, string, etc.
"""marks = [10, 20, 30, 40, 50]
student_mix = ["John", 10, 20, 30, 40, 50.1, True, False, None]
print(student_mix)

# list is mutable but string is not mutable like this
student_mix[0] = "Jane"
print(student_mix)

# list is ordered
print(student_mix[0])

#list slicing which is same as string slicing
#list_name = [starting_index : ending_index] #ending index is not included"""

#list methods
#append() - add item to the end of the list
# student_mix.append("Jane")
# print(student_mix)

#insert() - add item to the specific index
# student_mix.insert(2, "Jane")
# print(student_mix)

#remove() - remove the specific item means first occurence of the item
# student_mix = [1,2,"Jane",3,4,5]
# student_mix.remove("Jane")
# print(student_mix)

#remove the specific index
# student_mix.pop(2) #remove the index 2
# print(student_mix)

#sort() - sort the list
# student_mix.sort()
#student = [3,4,1,5]
#using sort method
"""student.sort()
print(student)
#without using sort method
for i in range(len(student)):
    for j in range(i+1, len(student)):
        if(student[i] > student[j]):
            temp = student[i]
            student[i] = student[j]
            student[j] = temp
print(student)"""

#reverse() - reverse the list

#using reverse method
"""student_mix.reverse()
print(student_mix)"""

#without using reverse method
"""student_mix = [1,2,3,4,5]
for i in range(len(student_mix)-1, -1, -1):
    print(student_mix[i])"""

#list.append(4) #add 4 to the end of the list
#print(list)

#list.sort() #sort the list
#print(list)
#list.sort(reverse=  True) #sort the list in reverse order(descending order)
#print(list)

#list.reverse() #reverse the list
#print(list)

#list.clear() #clear the list
#print(list)

#count() - count the specific item
#index() - get the index of the specific item
#clear() - clear the list

#list comprehension
#list_name = [expression for item in iterable if condition]

#list comprehension with if else
#list_name = [expression if condition else expression for item in iterable]

#list comprehension with nested loop


#tuple is a built in data type in python which is immutable sequence of values

#tuple_name = (value1, value2, value3)
#tuple_name = (1,2,3,4,5)
#tuple_name [0] = 10 #this will give error because tuple is immutable
#print(tuple_name)

#tuple methods
#count() - count the specific item
#index() - get the index of the specific item at first occurence

#tuple comprehension
#tuple_name = (expression for item in iterable if condition)