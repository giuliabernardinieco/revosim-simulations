import random
import os
import pandas as pd
import re
from tqdm import tqdm
import time
from sklearn.metrics.pairwise import pairwise_distances

# Folder Paths
# List of folder paths
folder_paths = ["/Users/gb4818/Desktop/REvoSim_output/30dp"]

# Define folder labels
folder_labels = [15]
# Extract the label from the folder_labels list
label = folder_labels[0]
COL_GENOME_INDEX = 0

out_filename = f"w50_{label}dp_genetic_diversity.csv"
print(f"writing to {out_filename}")

header_row = "Genome,Diversity,Simulation,dp"

with open(out_filename, "w") as out_file:
    out_file.write(f"{header_row}\n")
########################
###LOGS SPECIES COUNT###
########################


def genome_string_difference_count(genome_1: str, genome_2: str, cache: dict[str, str]) -> int:
    key = f"{genome_1}-{genome_2}"
    reverse_key = f"{genome_2}-{genome_1}"
    if key not in cache:
        cache[key] = sum(c1 != c2 for c1, c2 in zip(genome_1, genome_2))
        cache[reverse_key] = cache[key]
    return cache[key]


# Creating a function to create and store diversity values and return them in a table,
# from this table we will calculate stats for each sample
def diversity_table(genomes, num_pairs):
    # Select random pairs of indices
    random_indices = random.sample(range(len(genomes)), 2 * num_pairs)

    # Initialize a counter for differences
    differences_list = []

    # Compare strings in random pairs
    for i in range(0, len(random_indices), 2):
        index1, index2 = random_indices[i], random_indices[i + 1]
        string1, string2 = genomes.iloc[index1], genomes.iloc[index2]

        # Compare strings and count differences
        differences_count = genome_string_difference_count(string1, string2)

        # Append to the list
        differences_list.append((differences_count))

    return differences_list


for folder_i, folder_path in tqdm(enumerate(folder_paths)):
    # Loop through each file in the folder and read it into a DataFrame
    start = time.perf_counter()
    files_to_read = [
        filename
        for filename in os.listdir(folder_path)
        if re.match(r"REvoSim_individuals_data_.*\.txt", filename)
    ]
    time_taken = time.perf_counter() - start
    print(f"# of files = {len(files_to_read)}")
    print(f"time taken = {time_taken:0.3f}s")
    differences_list = []
    difference_cache = {}

    for file_j, filename in tqdm(enumerate(files_to_read[:1])):
        file_path = os.path.join(folder_path, filename)
        print(f"Reading from {file_path}")

        # read data
        start = time.perf_counter()
        
        with open(out_filename, "a") as out_file:
            start = time.perf_counter()
            df = pd.read_csv(file_path, sep=",", header=0, skiprows=12, usecols=[0])
            genomes = df["Genome"].to_list()
            genomes_sample = genomes[:len(genomes)//10]
            print(genomes[:5])
            print(len(genomes))
            print(len(set(genomes)))
            print(len(genomes_sample))
            for c1, gene_1 in tqdm(enumerate(genomes_sample)):
                for c2, gene_2 in enumerate(genomes_sample):
                    if c1 != c2:
                        differences_list.append(genome_string_difference_count(gene_1, gene_2, difference_cache))
            time_taken = time.perf_counter() - start
            print(f"time taken to process file {file_path} = {time_taken:0.3f}s")

# print(differences_list)
print(len(differences_list))
# df = pd.read_csv(out_filename)
# print(df.head())
# print(len(df))


# print("ALl done.")
