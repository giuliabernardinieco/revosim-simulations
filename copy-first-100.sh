#!/bin/bash

# Define the source folders
source_folders=(
    '/rds/general/user/gb4818/ephemeral/results_w50_35dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_6dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_4dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_5dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_10dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_50dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_25dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_40dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_3dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_8dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_20dp'
    '/rds/general/user/gb4818/ephemeral/results_w50_30dp'
)

# Define the destination folder
destination="/rds/general/user/gb4818/ephemeral/to-move"

# Create the destination folder if it doesn't exist
mkdir -p "$destination"

# Move the files with the suffix ajX from 1 to 100 from each folder to a new folder with the suffix 100
for folder in "${source_folders[@]}"; do
    folder_name=$(basename "$folder")
    new_folder_name="100_${folder_name}"
    mkdir -p "${destination}/${new_folder_name}"
    
    for i in {1..100}; do
        cp "${folder}"/*aj${i} "${destination}/${new_folder_name}"
    done
done

echo "Files copied successfully."