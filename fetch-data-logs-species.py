import random
import os
import pandas as pd
import re
from tqdm import tqdm
import time

# Folder Paths
# List of folder paths
folder_paths = ["/Users/gb4818/Desktop/REvoSim_output/30dp"]

# Define folder labels
folder_labels = [30]
# Extract the label from the folder_labels list
label = folder_labels[0]
COL_ITER_INDEX = 0
COL_SPECIES_COUNT_INDEX = 5


out_filename = f"w50_{label}dp_iterations_species_richness.csv"
print(f"writing to {out_filename}")

header_row = "Iteration_Number,Species_Count,Simulation,dp"

with open(out_filename, "w") as out_file:
    out_file.write(f"{header_row}\n")
########################
###LOGS SPECIES COUNT###
########################
# Create a list to store individual DataFrames

for folder_i, folder_path in tqdm(enumerate(folder_paths)):
    # Loop through each file in the folder and read it into a DataFrame
    start = time.perf_counter()
    files_to_read = [
        filename
        for filename in os.listdir(folder_path)
        if re.match(r"REvoSim_log_.*\.txt", filename)
    ]
    time_taken = time.perf_counter() - start
    print(f"# of files = {len(files_to_read)}")
    print(f"time taken = {time_taken:0.3f}s")

    for file_j, filename in tqdm(enumerate(files_to_read)):
        file_path = os.path.join(folder_path, filename)
        print(f"Reading from {file_path}")

        # read data
        with open(file_path, "r") as in_file, open(out_filename, "a") as out_file:
            start = time.perf_counter()
            line_counter = 0
            species_values_set = set()
            for line in in_file:
                if line_counter == 0:
                    # Skip first row which is header
                    line_counter += 1
                    continue
                
                line_cols = line.split(",")
                species_value = f"{line_cols[COL_ITER_INDEX]},{line_cols[COL_SPECIES_COUNT_INDEX]},{filename},{folder_labels[folder_i]}"
                if species_value not in species_values_set:
                    # do something
                    species_values_set.add(species_value)
                    out_file.write(f"{species_value}\n")
                
                line_counter += 1
            time_taken = time.perf_counter() - start
            print(len(species_values_set))
            print(f"time taken to process file {file_path} = {time_taken:0.3f}s") 

df = pd.read_csv(out_filename)
print(df.head())
print(len(df))


print("ALl done : )")
