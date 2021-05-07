#%%
import math 
with open ("data/data_5.txt") as file:
    data = [line.strip() for line in file]

#%%

def read_row(row):
    min_guess = 0
    max_guess = 127
    for letter in row:
        if letter == 'F':
            min_guess = min_guess
            max_guess = math.floor(min_guess + (max_guess - min_guess) /2)
        else:
            min_guess = math.ceil(min_guess + (max_guess - min_guess) /2)
            max_guess = max_guess
    return max_guess 
        
    
    
read_row(small_row)

#%%

def read_col(col):
    min_guess = 0
    max_guess = 7
    for letter in col:
        if letter == 'L':
            min_guess = min_guess
            max_guess = math.floor(min_guess + (max_guess - min_guess) /2)
        else:
            min_guess = math.ceil(min_guess + (max_guess - min_guess) /2)
            max_guess = max_guess
    return min_guess 
    
    
read_col(small_col)
  

#%%
# Part 1:

seat_id = []
for line in data:
    row = line[:-3]
    col = line[-3:]
    new_seat_id = read_row(row) * 8 + read_col(col)
    seat_id.append(new_seat_id) 
    
max(seat_id)


#%%
#Part 2

seat_id.sort()

count = seat_id[0]
for i in range(len(seat_id)):
    if count != seat_id[i]:
        break

    count += 1
    
print(count)
