import random
import os
import pandas as pd
import re

# Folder Paths
# List of folder paths
folder_paths = ['/Users/gb4818/Desktop/REvoSim_output/15dp',
                '/Users/gb4818/Desktop/REvoSim_output/30dp',]
# Define folder labels
folder_labels = [15, 30]

########################
###LOGS SPECIES COUNT###
########################
# Create a list to store individual DataFrames
dataframes = []

for i, folder_path in enumerate(folder_paths):
    # Loop through each file in the folder and read it into a DataFrame
    for filename in os.listdir(folder_path):
        match = re.match(r'REvoSim_log_.*\.txt', filename)
        if match:
            file_path = os.path.join(folder_path, filename)
            #df = pd.read_csv(file_path, sep=',', header=0, usecols=[0, 5], names=['Iteration_number', 'Species_count'])
            
            df = pd.read_csv(file_path, sep=',', header=0, usecols=[0, 5])
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Add 'simulation' and 'folder_label' columns
            df['Simulation'] = filename
            df['dp'] = folder_labels[i]
            
            # Append the modified DataFrame to the list
            dataframes.append(df)

# Concatenate all data in a pandas dataframe
combined_df = pd.concat(dataframes, ignore_index=True)
# save in a csv file
combined_df.to_csv('w50_xdp_iterations_species_richness.csv')

###############################
### LOGS ENVIRONMENT VALUES ###
###############################
# importing all data from all file so I have a table that I can access later. 
all_sin = []

for i, folder_path in enumerate(folder_paths):
    # creating a loop that will take all of the files, all of the individuals on a transect in the middle of the picture
    # create an empty dataframe to store the transects in the current folder
    colour_transects = pd.DataFrame(columns=['X coord', 'environment B value', 'Simulation'])
            
    for filename in os.listdir(folder_path):
        match = re.match(r'REvoSim_individuals_data_.*\.txt', filename)
        if match:
            file_path = os.path.join(folder_path, filename)
            # import file
            df = pd.read_csv(file_path, sep=',', header=0, skiprows=12, usecols=[1, 2, 11])
            # take all the records that have y = 49 (a transect in the middle)
            df = df[df['Y coord'] == 49]
            colour_cell = df[['X coord', 'environment B value']]
            colour_cell = colour_cell.drop_duplicates(subset=['X coord', 'environment B value'], keep='first')
            colour_cell['Simulation'] = filename
            
            colour_transects = pd.concat([colour_transects, colour_cell], ignore_index=True)
            colour_transects['dp'] = folder_labels[i]
    
    # Append the stats dataframe to the list
    all_sin.append(colour_transects)
# Concatenate all DataFrames from different folders into a single DataFrame
combined_colsin = pd.concat(all_sin, ignore_index=True)

# save in a csv file
combined_colsin.to_csv('w50_xdp_environment_values.csv')

###################################
### LOGS SPECIES RICHNESS GRIDS ###
###################################

# importing all data from all file so I have a table that I can access later. 
all_grids = []

for i, folder_path in enumerate(folder_paths):
    # creating a loop that will take all of the files, all of the individuals on a transect in the middle of the picture
    # create an empty dataframe to store the transects in the current folder
    grid = pd.DataFrame(columns=['X coord', 'Y coord', 'Species Richness', 'Simulation'])
            
    for filename in os.listdir(folder_path):
        match = re.match(r'REvoSim_individuals_data_.*\.txt', filename)
        if match:
            file_path = os.path.join(folder_path, filename)
            # import file
            df = pd.read_csv(file_path, sep=',', header=0, skiprows=12, usecols=[1, 2, 8])
            df = df[['X coord', 'Y coord', 'species ID']]
            # calculate species richness
            species_count = df.groupby(['Y coord', 'X coord'])['species ID'].nunique().reset_index()
            species_count['Simulation'] = filename
            species_count =species_count.rename(columns={'species ID': 'Species Richness'} )
            
            grid = pd.concat([grid, species_count], ignore_index=True)
            grid['dp'] = folder_labels[i]
            
    # Append the stats dataframe to the list
    all_grids.append(grid)
    
    
# Concatenate all DataFrames from different folders into a single DataFrame
grids = pd.concat(all_grids, ignore_index=True)
# save grids into a csv file
grids.to_csv('w50_xdp_grids_species_richness.csv')

# GENETIC DIVERSITY FUNCTIONS DEFINITION

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
        differences_count = sum(c1 != c2 for c1, c2 in zip(string1, string2))

        # Append to the list
        differences_list.append((differences_count))

    return differences_list

##############################
### LOGS GENETIC DIVERSITY ###
##############################

# Create a list to store individual DataFrames
dataframes = []

for i, folder_path in enumerate(folder_paths):
    # Create a list to store all the DataFrames for the current folder
    dfs = []
    
    # Loop through each file in the folder and read it into a DataFrame
    for filename in os.listdir(folder_path):
        match = re.match(r'REvoSim_individuals_data_.*\.txt', filename)
        if match:
            file_path = os.path.join(folder_path, filename)

            # Read the DataFrame from the file
            df = pd.read_csv(file_path, sep=',', header=0, skiprows=12,  usecols=[0])
            genomes = df['Genome']
            # keep the first 32 bits from each genome
            #genomes = df['Genome'].str[:32]
            #remove the first 32 and keep the last
            #genomes = df['Genome'].str[32:]
            
            # Calculate genetic diversity and store in the list
            diversity_list = diversity_table(genomes, len(genomes) // 2)

            # Create a DataFrame with an additional 'File' column
            div_df = pd.DataFrame({'Diversity': diversity_list, 'dp': folder_labels[i], 'Simulation': filename})
            dfs.append(div_df)

    # Concatenate all DataFrames in the list
    combined_df_folder = pd.concat(dfs, ignore_index=True)
    dataframes.append(combined_df_folder)

# Concatenate all DataFrames from different folders into a single DataFrame
diversity = pd.concat(dataframes, ignore_index=True)
# Let's create a table with average diversity for each simulation
average_div_df = diversity.groupby(['dp','Simulation'])['Diversity'].mean().reset_index()
average_div_df.to_csv('w50_xdp_genetic_diversity.csv')