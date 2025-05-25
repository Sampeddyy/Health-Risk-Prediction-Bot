import os
import pandas as pd
from datetime import datetime, timedelta

# Constants
BASE_DIR = r"S:\btp"
FOLDER_NAME = "Person Calories Data"
BASE_FOLDER_PATH = os.path.join(BASE_DIR, FOLDER_NAME)
PERSON_DATA_FILE = os.path.join(BASE_DIR, "Generated_People_Data.xlsx")
NUTRITION_DB_FILE = os.path.join(BASE_DIR, "ALL ITEMS", "cleaned_merged_unique_output.xlsx")

# Load person data and nutrition database
person_data = pd.read_excel(PERSON_DATA_FILE)
nutrition_db = pd.read_excel(NUTRITION_DB_FILE)

# Login function
def login():
    print("Login to access your daily calorie tracker.")
    name = input("Enter your name: ").strip()
    dob = input("Enter your date of birth (YYYY-MM-DD): ").strip()
    password = name + dob
    
    person = person_data[(person_data["Name"] == name) & 
                         (person_data["Date of Birth"] == dob)]
    if not person.empty:
        print(f"Welcome, {name}!")
        return person.iloc[0]
    else:
        print("Invalid login details. Please try again.")
        return login()

# Parse meal details into food items and quantities
def parse_meal(meal):
    if meal.lower() == "skipped":
        return []
    
    meal = meal.replace("'", "").replace(",", " ").strip()
    while "  " in meal:
        meal = meal.replace("  ", " ")
    
    parts = meal.split()
    parsed = []
    i = 0
    while i < len(parts):
        if parts[i].replace(".", "").isdigit() and i + 3 <= len(parts) and parts[i + 1] == "gm" and parts[i + 2] == "of":
            quantity = float(parts[i]) / 100
            food_item = "100 gm of " + " ".join(parts[i + 3:i + 4])
            parsed.append((quantity, food_item))
            i += 4
        else:
            i += 1
    return parsed

# Calculate nutritional totals
def calculate_nutrition(parsed_meals):
    totals = {"Carbohydrate": 0.0, "Fiber": 0.0, "Sugar": 0.0, "Fat": 0.0, "Saturated Fat": 0.0,
              "Polyunsaturated Fat": 0.0, "Monounsaturated Fat": 0.0, "Trans Fat": 0.0,
              "Cholesterol": 0.0, "Sodium": 0.0, "Potassium": 0.0, "Vitamin A": 0.0,
              "Calcium": 0.0, "Iron": 0.0}
    
    for quantity, food_item in parsed_meals:
        lookup_key = " ".join(food_item.lower().split())
        db_key = nutrition_db["Food Item"].str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)
        db_row = nutrition_db[db_key == lookup_key]
        if not db_row.empty:
            for nutrient in totals.keys():
                totals[nutrient] += float(db_row[nutrient].iloc[0]) * quantity
    return totals

# Get the week start (Monday) for a given date
def get_week_start(date_str):
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    days_to_monday = (date_obj.weekday()) % 7
    week_start = date_obj - timedelta(days=days_to_monday)
    return week_start.strftime("%d/%m/%Y")

# Log meals and update nutrient summary
def log_meals(person_id, person_name):
    person_folder = os.path.join(BASE_FOLDER_PATH, f"{person_name}_{person_id}")
    os.makedirs(person_folder, exist_ok=True)
    
    meal_file = os.path.join(person_folder, f"meals_{person_name}_{person_id}.xlsx")
    nutrient_file = os.path.join(person_folder, f"nutrients_{person_name}_{person_id}.xlsx")
    
    print(f"Logging meals for {person_name} (ID: {person_id}).")
    date = datetime.now().strftime("%d/%m/%Y")
    week_start = get_week_start(date)
    
    sections = ["Morning", "Lunch", "Dinner", "Snacks", "Others"]
    daily_meals = []

    # Load existing data if it exists
    existing_meals = pd.DataFrame()
    if os.path.exists(meal_file):
        existing_meals = pd.read_excel(meal_file)
        today_meals = existing_meals[existing_meals["Date"] == date]
    else:
        today_meals = pd.DataFrame()

    print(f"Input your detailed daily meal plan for {date}:")
    for section in sections:
        current_meal = "Skipped"
        if not today_meals.empty and section in today_meals["Section"].values:
            current_meal = today_meals[today_meals["Section"] == section]["Meal Details"].iloc[0]
            print(f"\nCurrent {section} entry: '{current_meal}'")
        
        print(f"Enter new meal details for {section} (or press Enter to keep current):")
        print("Example: '100 gm of milk 100 gm of paneer'")
        print("Type 'NA' to skip this meal.")
        meal = input(f"{section}: ").strip()
        
        if meal == "":
            meal = current_meal
        elif meal.lower() == "na":
            meal = "Skipped"
        
        daily_meals.append({"Date": date, "Section": section, "Meal Details": meal})
    
    # Save meal log
    new_meal_data = pd.DataFrame(daily_meals)
    if os.path.exists(meal_file):
        existing_meal_data = pd.read_excel(meal_file)
        filtered_meal_data = existing_meal_data[
            ~((existing_meal_data["Date"] == date) & (existing_meal_data["Section"].isin(new_meal_data["Section"])))
        ]
        updated_meal_data = pd.concat([filtered_meal_data, new_meal_data], ignore_index=True)
    else:
        updated_meal_data = new_meal_data
    updated_meal_data.to_excel(meal_file, index=False)
    print(f"Meal log saved to '{meal_file}'.")

    # Calculate daily nutrients and update weekly summary
    daily_nutrients = []
    for _, row in new_meal_data.iterrows():
        if row["Meal Details"] != "Skipped":
            parsed_meals = parse_meal(row["Meal Details"])
            nutrition_totals = calculate_nutrition(parsed_meals)
            daily_nutrients.append(nutrition_totals)
    
    if daily_nutrients:
        daily_total = pd.DataFrame(daily_nutrients).sum().to_dict()
        daily_total["Week Start"] = week_start
        
        if os.path.exists(nutrient_file):
            existing_nutrient_data = pd.read_excel(nutrient_file)
            for col in existing_nutrient_data.columns:
                if col != "Week Start":
                    existing_nutrient_data[col] = existing_nutrient_data[col].astype(float)
            if week_start in existing_nutrient_data["Week Start"].values:
                idx = existing_nutrient_data[existing_nutrient_data["Week Start"] == week_start].index[0]
                for key in daily_total:
                    if key != "Week Start" and key in existing_nutrient_data.columns:
                        existing_nutrient_data.loc[idx, key] = float(daily_total[key])
                updated_nutrient_data = existing_nutrient_data
            else:
                updated_nutrient_data = pd.concat([existing_nutrient_data, pd.DataFrame([daily_total])], ignore_index=True)
        else:
            updated_nutrient_data = pd.DataFrame([daily_total])
            for col in updated_nutrient_data.columns:
                if col != "Week Start":
                    updated_nutrient_data[col] = updated_nutrient_data[col].astype(float)
        
        updated_nutrient_data.to_excel(nutrient_file, index=False)
        print(f"Nutrient summary updated in '{nutrient_file}'.")
    else:
        print("No nutrients calculated - all meals skipped.")

# Main program
def main():
    person = login()
    person_id = person["Person ID"]
    person_name = person["Name"]
    log_meals(person_id, person_name)

if __name__ == "__main__":
    main()
