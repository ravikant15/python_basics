#loops in python

#loops are used to repeat the instructions

"""while loop

    while condition:
        instructions
        increment/decrement
"""
i=1
while i<10:
    print(i)
    i+=1
print(i)

#for loop
nums = [1,2,3,4,5,6,7,8,9,10]
for i in nums:
    print(i)

#nested loop
for i in range(1,10):
    for j in range(1,10):
        print(i,j)

#break statement
for i in range(1,10):
    if i==5:
        break
    print(i)

#continue statement
for i in range(1,10):
    if i==5:
        continue
    print(i)

#pass statement
for i in range(1,10):
    pass

#range function is used to generate a sequence of numbers from start to end start from 0 by default
#range(start,end,step)
#step is the difference between the numbers in the sequence
#step is 1 by default
#end is not included in the sequence
#start is included in the sequence
#end is not included in the sequence
for i in range(1,10):
    print(i)

#enumerate function
#enumerate function is used to get the index of the element in the sequence
#enumerate(sequence)
#sequence is the sequence of the elements
#index is the index of the element in the sequence
#element is the element in the sequence
for i,j in enumerate(range(1,10)):
    print(i,j)

#zip function
#zip function is used to combine two sequences
#zip(sequence1,sequence2)
#sequence1 is the first sequence
#sequence2 is the second sequence
#zip function returns a tuple of the elements of the two sequences
for i,j in zip(range(1,10),range(1,10)):
    print(i,j)