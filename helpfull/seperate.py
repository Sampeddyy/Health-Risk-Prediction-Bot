import pandas as pd
import os

# Path to the original file
input_file = r"S:\btp\Unique_Food_Categories.xlsx"

# Read the original Excel file
df = pd.read_excel(input_file)

# Get unique categories from the 'Category' column
categories = df['Category'].unique()

# Loop through each category and create a folder for it
for category in categories:
    # Create a sanitized version of the category name for folder creation
    category_folder = category.strip().replace(" ", "_").replace("/", "_")
    
    # Full path for the new folder
    category_folder_path = os.path.join(r"S:\btp", category_folder)
    
    # Create the category folder if it doesn't already exist
    if not os.path.exists(category_folder_path):
        os.makedirs(category_folder_path)
    
    # Filter the data for the current category
    category_data = df[df['Category'] == category]
    
    # Create a safe filename for the Excel file
    file_name = category_folder + ".xlsx"
    
    # Full path to save the Excel file for this category
    output_file = os.path.join(category_folder_path, file_name)
    
    # Write the category data to an Excel file
    category_data.to_excel(output_file, index=False)

   

print("All files and folders created successfully.")
