import requests
import pandas as pd
import os

# API Credentials
app_id = "a79d9d1c"
app_key = "326083faf23dcd0d804f5489385f268d"

# API Endpoint
url = "https://api.edamam.com/api/nutrition-data"

# Root Folder Location
root_folder = r"S:\\btp\\ALL ITEMS"

# Iterate over the subfolders in the root folder
for subdir, _, files in os.walk(root_folder):
    for file in files:
        # Check if the file is an Excel file
        if file.endswith(".xlsx"):
            input_file = os.path.join(subdir, file)
            
            # Create the output file name by appending "_NutritionalData" to the original file name
            output_file = os.path.join(subdir, f"{os.path.splitext(file)[0]}_NutritionalData.xlsx")

            # Load the food items from the Excel file
            food_items = pd.read_excel(input_file)

            # Create a list to store the nutritional data
            data = []

            # Iterate through each food item
            for index, row in food_items.iterrows():
                food = f"100 gm of {row['Food Item']}"  # Adjust to include "100 gm of" in the food item
                category = row["Category"]  # Added to capture the category
                params = {
                    "app_id": app_id,
                    "app_key": app_key,
                    "ingr": food
                }

                # Send a request to the API
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    # Parse the response
                    response_data = response.json()
                    nutrients = response_data.get("totalNutrients", {})

                    # Extract required details
                    nutritional_info = {
                        "Food Item": food,
                        "Category": category,  # Include the category in the output
                        "Carbohydrate": nutrients.get("CHOCDF", {}).get("quantity", "N/A"),
                        "Fiber": nutrients.get("FIBTG", {}).get("quantity", "N/A"),
                        "Sugar": nutrients.get("SUGAR", {}).get("quantity", "N/A"),
                        "Fat": nutrients.get("FAT", {}).get("quantity", "N/A"),
                        "Saturated Fat": nutrients.get("FASAT", {}).get("quantity", "N/A"),
                        "Polyunsaturated Fat": nutrients.get("FAPU", {}).get("quantity", "N/A"),
                        "Monounsaturated Fat": nutrients.get("FAMS", {}).get("quantity", "N/A"),
                        "Trans Fat": nutrients.get("FATRN", {}).get("quantity", "N/A"),
                        "Cholesterol": nutrients.get("CHOLE", {}).get("quantity", "N/A"),
                        "Sodium": nutrients.get("NA", {}).get("quantity", "N/A"),
                        "Potassium": nutrients.get("K", {}).get("quantity", "N/A"),
                        "Vitamin A": nutrients.get("VITA_RAE", {}).get("quantity", "N/A"),
                        "Calcium": nutrients.get("CA", {}).get("quantity", "N/A"),
                        "Iron": nutrients.get("FE", {}).get("quantity", "N/A"),
                    }

                    data.append(nutritional_info)
                else:
                    print(f"Error fetching data for {food}: {response.status_code}")

            # Create a DataFrame from the collected data
            df = pd.DataFrame(data)

            # Save the DataFrame to a new Excel file in the same folder with the new name
            df.to_excel(output_file, index=False)

            print(f"Nutritional data for {file} has been saved to {output_file}")
