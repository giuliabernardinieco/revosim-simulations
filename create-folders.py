import os

# Specify the path where you want to create the folders
base_path = '/Users/gb4818/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Rev-res-in/environments'
numbers = [4, 5, 10, 25, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 200]

# Create 50 folders
for i in numbers:
    folder_name = f'w{i}'
    folder_path = os.path.join(base_path, folder_name)
    
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created successfully at {folder_path}")
    except OSError as e:
        print(f"Failed to create folder '{folder_name}': {e}")