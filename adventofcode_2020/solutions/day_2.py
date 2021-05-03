#%%
  
with open("2.txt") as file:
    data = [line for line in file]

data[0]

#%%
# Part 1 ===
part1 = 0
for entry in data:

    entry = entry.split()
    numbers = entry[0].split(sep="-")

    minimum = int(numbers[0])
    maximum = int(numbers[1])

    letter = entry[1][0]
    password = entry[2]

    if minimum <= password.count(letter) <= maximum:
        part1 += 1

print(part1)

#%%
# Part 2 ===
part2 = 0
for entry in data:

    entry = entry.split()
    numbers = entry[0].split(sep="-")

    minimum = int(numbers[0])-1
    print(minimum)
    maximum = int(numbers[1])-1

    letter = entry[1][0]
    password = list(entry[2])
    
    

    if password[minimum] == letter and password[maximum] == letter:
        part2 += 1
        
        #    elif password[minimum] == letter or password[maximum] == letter:
        
        
#%%

test = 'test'
test[2]