file_path = 'ID/unique_ids.txt'  

# Assuming all elements are on a single line, separated by a comma  
with open(file_path, 'r') as file:  
    # Read the entire file as a single string and split by comma  
    real_list = file.read().strip().split(',')  

# Remove whitespace from each element if necessary  
real_list = [element.strip() for element in real_list]  

file_path = 'ID/divorce_id.txt'  

# Assuming all elements are on a single line, separated by a comma  
with open(file_path, 'r') as file:  
    # Read the entire file as a single string and split by comma  
    divorce_list = file.read().strip().split(',')  

# Remove whitespace from each element if necessary  
divorce_list = [element.strip() for element in divorce_list]  


file_path = 'ID/lien_id.txt'  

# Assuming all elements are on a single line, separated by a comma  
with open(file_path, 'r') as file:  
    # Read the entire file as a single string and split by comma  
    lien_list = file.read().strip().split(',')  

# Remove whitespace from each element if necessary  
lien_list = [element.strip() for element in lien_list]  

file_path = 'ID/bankruptcy_id.txt'  

# Assuming all elements are on a single line, separated by a comma  
with open(file_path, 'r') as file:  
    # Read the entire file as a single string and split by comma  
    bankruptcy_list = file.read().strip().split(',')  

# Remove whitespace from each element if necessary  
bankruptcy_list = [element.strip() for element in bankruptcy_list]  

set1 = set(real_list)
set2 = set(lien_list)
set3 = set(bankruptcy_list)
set4 = set(divorce_list)

# Find the difference  
result_list = list(set1 - set2)

# Open the file in write mode  
with open('ID/result.txt', 'w') as file:  
    # Join the elements with a comma and write to the file  
    file.write(','.join(result_list))  
    
print(len(result_list))  