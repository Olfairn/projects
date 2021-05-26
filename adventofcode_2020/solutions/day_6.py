#%%
from os import replace


with open ("data/data_6.txt") as file:
    data = [line.strip() for line in file]
    
data.append("")

data
#%%
# Parse the data into list of groups
groups, group = [], []

for line in data:
    if line == "":
        groups.append(group)
        group = []

    else:
        group.append(line)

#%% 

# Merge groups 
merged_groups = [group.append("") for group in groups]

#%%
merged_groups = groups.append("")
merged_groups

#%%
len(set('/ae'))