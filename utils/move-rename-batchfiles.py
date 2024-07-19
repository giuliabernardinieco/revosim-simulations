import os

source_folder = "/Users/gb4818/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Rev-res-in/2nd batches - Blue channel/1over50-bis/mh"
destination_folder = "/Users/gb4818/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Rev-res-in/1over50/mh"

#checking if the folder exists, otherwise create one
os.makedirs(destination_folder, exist_ok=True)

for i in range(1, 31):
    old_filename = f"REvoSim_log_{i}.txt"
    new_filename = f"REvoSim_log_{i + 80}.txt"
    source_path = os.path.join(source_folder, old_filename)
    destination_path = os.path.join(destination_folder, new_filename)
    
    os.rename(source_path, destination_path)
    print(f"Moved {old_filename} to {destination_path}")

for i in range(1, 31):
    old_filename = f"REvoSim_individuals_data_{i}.txt"
    new_filename = f"REvoSim_individuals_data_{i + 80}.txt"
    source_path = os.path.join(source_folder, old_filename)
    destination_path = os.path.join(destination_folder, new_filename)
    
    os.rename(source_path, destination_path)
    print(f"Moved {old_filename} to {destination_path}")
