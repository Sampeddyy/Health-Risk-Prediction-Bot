import pandas as pd

# Function to get input for each meal section
def get_meal_input(section_name):
    print(f"\nEnter your meal details for {section_name}:")
    print("Example: '100 ml of milk 100 gm of oats 100 gm of peanut butter'")
    print("If you are skipping this meal, type 'NA'.")
    
    meal = input(f"{section_name}: ").strip()
    if meal.lower() == "na":
        return {"Section": section_name, "Meal Details": "Skipped"}
    elif meal:
        return {"Section": section_name, "Meal Details": meal}
    else:
        print("Invalid input. Please enter a valid meal description or 'NA'.")
        return get_meal_input(section_name)

# Main program
def main():
    sections = ["Morning", "Lunch", "Dinner", "Snacks", "Others"]
    daily_meals = []
    
    print("Input your detailed daily meal plan:")
    for section in sections:
        daily_meals.append(get_meal_input(section))
    
    # Create a DataFrame
    df = pd.DataFrame(daily_meals)
    
    # Save to Excel
    output_file = "detailed_daily_meal_plan.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\nYour detailed daily meal plan has been saved to '{output_file}'.")

# Run the program
if __name__ == "__main__":
    main()
