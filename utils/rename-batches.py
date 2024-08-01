import os

# Directory containing the files
directory = '/rds/general/user/gb4818/ephemeral/results_w50_20dp_TEST'

# Mapping of current numbers to new numbers
mapping = {
    1: 30, 2: 101, 3: 124, 4: 128, 5: 217, 6: 365, 7: 527, 8: 557, 9: 758, 10: 893,
    11: 1028, 12: 1319, 13: 1416, 14: 1523, 15: 1555, 16: 1557, 17: 1573, 18: 1597,
    19: 1613, 20: 1646, 21: 1678, 22: 1691, 23: 1773, 24: 1789, 25: 1809, 26: 1812,
    27: 1956, 28: 1973, 29: 2011, 30: 2122, 31: 2682, 32: 2718, 33: 2790, 34: 2798,
    35: 2821, 36: 2847, 37: 2858, 38: 2965, 39: 3001
}

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.startswith("REvoSim_log_envw50_20dp_aj") and filename.endswith(".txt"):
        # Extract the number after "aj"
        current_number = int(filename.split("aj")[1].split(".")[0])
        
        # Get the new number from the mapping
        new_number = mapping.get(current_number)
        
        if new_number is not None:
            # Create the new filename
            new_filename = filename.replace(f'aj{current_number}', f'aj{new_number}')
            
            # Full paths for renaming
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed: {filename} to {new_filename}')
