import os
import pandas as pd

# Function to merge all Excel files with '_NutritionalData' in the filename and keep only unique elements
def merge_excel_files_unique(folder_path, output_file):
    # List to store all dataframes
    all_data = []
    
    # Walk through all files in the folder and subfolders
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Check if the file is an Excel file and contains '_NutritionalData' in the filename
            if filename.endswith('.xlsx') and '_NutritionalData' in filename:
                file_path = os.path.join(root, filename)
                
                # Read the Excel file
                df = pd.read_excel(file_path)
                
                # Append the dataframe to the list
                all_data.append(df)
                print(f"Added {filename} from {root} to the merge list.")
    
    # Concatenate all dataframes into a single dataframe
    merged_data = pd.concat(all_data, ignore_index=True)
    
    # Drop duplicate rows (based on all columns)
    merged_data_unique = merged_data.drop_duplicates()
    
    # Save the merged data (with unique elements) to a new Excel file
    merged_data_unique.to_excel(output_file, index=False)
    print(f"All '_NutritionalData' files merged and unique elements saved to {output_file}")

# Specify the folder path and output file name
folder_path = r"S:\btp\ALL ITEMS"  # Your updated folder path
output_file = r"S:\btp\ALL ITEMS\merged_unique_output.xlsx"  # Output file path

# Run the merge function
merge_excel_files_unique(folder_path, output_file)
