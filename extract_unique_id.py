import ast  

def get_unique_ids_from_list(filename):  
    with open(filename, 'r') as file:  
        # Read the list from the file and convert it to a Python list  
        ids_list = file.read()  
        ids = ast.literal_eval(ids_list)  # Safely evaluate the string to a list  
        print(f"Total IDs in list: {len(ids)}")  
    
    # Extract unique IDs using a set  
    unique_ids = set(ids)  
    print(f"Number of unique IDs: {len(unique_ids)}")  

    return unique_ids  

def save_unique_ids(input_file, output_file):  
    # Get unique IDs  
    unique_ids = get_unique_ids_from_list(input_file)  
    
    # Write these unique IDs to another file  
    with open(output_file, 'w') as file:  
        for id in unique_ids:  
            file.write(f"{id}\n")  
    
    print(f"Unique IDs have been saved to {output_file}.")  

if __name__ == "__main__":  
    input_file = "id.txt"  
    output_file = "unique_ids.txt"  
    save_unique_ids(input_file, output_file)