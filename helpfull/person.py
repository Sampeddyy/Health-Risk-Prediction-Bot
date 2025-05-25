import pandas as pd
import random
from datetime import datetime, timedelta

# List of common Indian first names
first_names = [
    "Aarav", "Aditi", "Akash", "Ananya", "Arjun", "Deepak", "Divya", "Gaurav", 
    "Harsha", "Ishita", "Karan", "Kavya", "Lakshmi", "Meera", "Neha", "Nikhil", 
    "Pooja", "Priya", "Ramesh", "Rhea", "Rohit", "Sanjay", "Sneha", "Sunil", "Vivek"
]

# List of common Indian surnames
surnames = [
    "Agarwal", "Bansal", "Bhat", "Bhardwaj", "Chauhan", "Desai", "Gupta", "Iyer", 
    "Jain", "Kapoor", "Kumar", "Mehta", "Mishra", "Nair", "Patel", "Reddy", "Rao", 
    "Shah", "Sharma", "Singh", "Soni", "Suri", "Tiwari", "Verma", "Yadav", "Chatterjee", 
    "Choudhury", "Das", "Dutta", "Joshi", "Khan", "Khatri", "Lamba", "Malhotra", "Pandey", 
    "Parikh", "Rathi", "Saxena", "Sehgal", "Sharma", "Srivastava", "Thakur", "Vaidya", 
    "Vyas", "Zaveri", "Agrawal", "Bhagat", "Chowdhury", "Kaur", "Ranjan"
]

# Function to generate a random proper name
def generate_name():
    first_name = random.choice(first_names)
    surname = random.choice(surnames)
    return f"{first_name} {surname}"

# Function to generate random dates of birth (between 1995 and 2010)
def random_dob(start_year=1995, end_year=2010):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date

# Function to calculate BMR
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100  # Convert cm to meters
    return weight / (height_m ** 2)

# Generate 100 random people data
people_data = []
for person_id in range(1, 101):
    name = generate_name()
    dob = random_dob()
    age = datetime.now().year - dob.year  # Calculate age from the current year
    weight = random.uniform(50, 100)  # Random weight between 50kg and 100kg
    height = random.uniform(150, 200)  # Random height between 150cm and 200cm
    gender = random.choice(["Male", "Female"])
    bmr = calculate_bmr(weight, height, age, gender)
    bmi = calculate_bmi(weight, height)
    people_data.append({
        "Person ID": person_id,
        "Name": name,
        "Date of Birth": dob.strftime("%Y-%m-%d"),
        "Age": age,
        "Weight (kg)": round(weight, 2),
        "Height (cm)": round(height, 2),
        "Gender": gender,
        "BMR (kcal/day)": round(bmr, 2),
        "BMI": round(bmi, 2)
    })

# Convert to DataFrame
df = pd.DataFrame(people_data)

# Save to Excel file
output_path = "S:/btp/Generated_People_Data.xlsx"  # Update with a valid directory
df.to_excel(output_path, index=False)
print(f"Data saved successfully to {output_path}")

# To add new entries interactively, uncomment the following block
while True:
    person_id = df["Person ID"].max() + 1
    name = input("Enter name: ").capitalize()
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    dob = datetime.strptime(dob, "%Y-%m-%d")
    age = datetime.now().year - dob.year
    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (cm): "))
    gender = input("Enter gender (Male/Female): ").capitalize()
    bmr = calculate_bmr(weight, height, age, gender)
    bmi = calculate_bmi(weight, height)

    # Append the new entry to the DataFrame
    new_entry = {
        "Person ID": person_id,
        "Name": name,
        "Date of Birth": dob.strftime("%Y-%m-%d"),
        "Age": age,
        "Weight (kg)": round(weight, 2),
        "Height (cm)": round(height, 2),
        "Gender": gender,
        "BMR (kcal/day)": round(bmr, 2),
        "BMI": round(bmi, 2)
    }
    df = df.append(new_entry, ignore_index=True)

    # Ask user if they want to add more entries
    more = input("Do you want to add another entry? (yes/no): ").lower()
    if more != "yes":
        break

# Save the updated DataFrame back to Excel
df.to_excel(output_path, index=False)
print(f"Data saved successfully to {output_path}")

