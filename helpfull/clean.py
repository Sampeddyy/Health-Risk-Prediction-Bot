import pandas as pd

# Load the data from the original Excel file
file_path = r'S:\btp\Indian_Food_Categories.xlsx'
df = pd.read_excel(file_path)

# Create lists to store the food items and their corresponding categories
food_items = []
categories = []

# Loop through each column (which represents a category) and extract the food items
for category, column in df.items():
    for food_item in column.dropna():  # skip NaN values
        food_items.append(food_item)
        categories.append(category)

# Create a DataFrame with the flattened data
result_df = pd.DataFrame({
    'Food Item': food_items,
    'Category': categories
})

# Remove duplicate food items while preserving the first occurrence (order)
result_df = result_df.drop_duplicates(subset='Food Item', keep='first')

# Define the output file path
output_file_path = r'S:\btp\Unique_Food_Categories.xlsx'

# Save the result into a new Excel file
result_df.to_excel(output_file_path, index=False)

# Print confirmation that the file has been saved
print(f"New file created with unique food items and saved to: {output_file_path}")
