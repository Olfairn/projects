#%%
  
from os import sep


with open("data/data_4.txt") as file:
    data = [line for line in file]
    
data[:5]
#%%

#Part 1 
#? 1. Split the passport
join_passport = []
join_passport = "".join(data)

split_passport = join_passport.split(sep="\n\n")

#%%
#? 2. Split the components 
total_valid = 0
for fields in split_passport:
    split_field = fields.split() 
    if len(split_field) == 8:
        total_valid += 1
    elif len(split_field) == 7 and any(s.startswith('cid') for s in split_field) == False:
        total_valid += 1

print(total_valid)

# %%

#Part 2

def valid_byr(byr):
    return len(str(byr)) == 4 and 1920 <= int(byr) <= 2002

def valid_iyr(iyr):
    return len(str(iyr)) == 4 and 2010 <= int(iyr) <= 2020

def valid_eyr(eyr):
    return len(str(eyr)) == 4 and 2020 <= int(eyr) <= 2030

def valid_hgt(hgt):
    return hgt[-2:] == 'cm' and 150 <= int(hgt[:-2]) <= 193 or hgt[-2:] == 'in'and 59 <= int(hgt[:-2]) <= 76

def valid_hcl(hcl):
    accepted_alpha = ['a','b','c','d','e','f']
    
    for character in hcl[1:]:
        if (character.isnumeric() or (character in accepted_alpha)) == False:
            return False
    if hcl[0] == '#' and len(hcl) == 7:
        return True
    else:
        return False

def valid_ecl(ecl):
    return ecl in ['amb','blu','brn','gry','grn','hzl','oth']

def valid_pid(pid):
    return len(str(pid)) == 9 and pid.isnumeric() == True 

def full_valid(any):
    if any[:3] == 'byr':
        return valid_byr(any[4:]) 
    if any[:3] == 'iyr':
        return valid_iyr(any[4:])
    if any[:3] == 'eyr':
        return valid_eyr(any[4:])
    if any[:3] == 'hgt':
        return valid_hgt(any[4:])
    if any[:3] == 'hcl':
        return valid_hcl(any[4:])
    if any[:3] == 'ecl':
        return valid_ecl(any[4:])
    if any[:3] == 'pid':
        return valid_pid(any[4:])
    else:
        False

#%%


valid1 = []
for fields in split_passport:
    split_field = fields.split() 
    if len(split_field) == 8:
        valid1.append(split_field)
    elif len(split_field) == 7 and any(s.startswith('cid') for s in split_field) == False:
        valid1.append(split_field)

#%%
count_valid2 = 0

for passport in valid1:
    if False not in list_check:
        count_valid2 += 1
    list_check = []
    for check2 in passport:   
        valid = full_valid(check2)
        list_check.append(valid)

count_valid2
