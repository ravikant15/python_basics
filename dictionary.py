#dictionary is a collection of key-value pairs
#key-value pairs are unordered and mutable (changable) and donot allow duplicate keys
#we can make a tuple as a key in a dictionary but not a list because list is mutable and tuple is immutable

#creating a dictionary
"""dict = {
    "name": "John",
    "age": 20,
    "city": "New York",
    "marks": [10,20,30,40,50],
    "list": (1,2,3,4,5)
}"""

#print(dict)

#accessing the value of the dictionary
# print(dict["name"])
# print(dict["age"])

#nested dictionary
dict = {
    "name": "John",
    "age": 20,
    "marks": {
        "math": 100,
        "science": 90,
        "english": 80
    }
}

#dictionary methods
#keys() - return all the keys of the dictionary
print(dict.keys())

#values() - return all the values of the dictionary
print(dict.values())

#items() - return all the key-value pairs of the dictionary
print(dict.items())

#update() - update the dictionary
print(dict.update({"city": "New York"}))

#get() - return the value of the key
print(dict.get("city"))

""" set in python
"""

# set is a collection of unordered and unindexed elements
# each element in set is unique and immutable

nums = {1,2,3,4,5,6,7,8,9,10}
set2 = {1,2,2,2}

#the set2 will be {1,2} because 2 is duplicate and it will be ignored
#to create a empty set we use set()
empty_set = set()


#set methods
#add() - add an element to the set
nums.add(11)
print(nums)

#remove() - remove an element from the set
nums.remove(11)
print(nums)

#clear() - clear the set
nums.clear()
print(nums)

#union() - return a new set with all the elements of the two sets
nums1 = {1,2,3,4,5}
nums2 = {6,7,8,9,10}
print(nums1.union(nums2))

#intersection() - return a new set with all the elements that are common to both sets
print(nums1.intersection(nums2))

#difference() - return a new set with all the elements that are in the first set but not in the second set
print(nums1.difference(nums2))
