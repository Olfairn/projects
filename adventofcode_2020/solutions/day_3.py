#%%
  
with open("3.txt") as file:
    data = [line for line in file]

data
#%%
# Part 1 ===
# add 3 step to each row and check if . or # 
# if sum step > lengt -> subtrack the lengh

line = 0
position = 0 
tree = 0
for steps in data:
    if position >= len(steps)-1: # -1 to account for the \n
        position -= len(steps)-1
    if data[line][position] == "#":
        tree += 1
           
    line += 1
    position += 3

print(tree)

#%%
# Part 2 

def slope(input, right, down):
    line = 0
    position = 0 
    tree = 0
    for steps in input:
        if line > len(input):
            break
        if position >= len(steps)-1: # -1 to account for the \n
            position -= len(steps)-1
        if data[line][position] == "#":
            tree += 1

        line += down
        position += right
    
    return tree
    
slope(data,3,1) * slope(data,1,1) * slope(data,5,1) * slope(data,7,1) * slope(data,1,2)

#%%
len(data)-2
