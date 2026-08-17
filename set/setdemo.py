s1 = {1,2,3,4,10,1,2}
s2=set([1,2,3,4,1,2])

print(s1)
print(s2)
s1.add(100)
print(s1)
s2.add("tops")
print(s2)

print(s2 ^ s1) #Elements that are in either set but NOT in both.
print(s2 - s1) #Elements in s2 but NOT in s1.
print(s2 & s1) #Elements common in both sets.

print(s2 | s1) # all 

s1.remove(1)
print(s1)
#s1.remove(1000) showing error bcoz 1000 not inside 

s1.discard(1000) #not showing 
print(s1)
