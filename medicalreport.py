import os
import pandas as pd
import PyPDF2
import re

# Constants
BASE_DIR = r"S:\btp"
FOLDER_NAME = "Person Calories Data"
BASE_FOLDER_PATH = os.path.join(BASE_DIR, FOLDER_NAME)
PERSON_DATA_FILE = os.path.join(BASE_DIR, "Generated_People_Data.xlsx")

person_data = pd.read_excel(PERSON_DATA_FILE)

def login():
    print("Login to access your medical report input system.")
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

def check_or_create_folder(person_id, person_name):
    person_folder = os.path.join(BASE_FOLDER_PATH, f"{person_name}_{person_id}")
    if not os.path.exists(person_folder):
        print(f"No calorie intake folder found for {person_name} (ID: {person_id}).")
        create = input("Would you like to create one? (yes/no): ").strip().lower()
        if create == "yes":
            os.makedirs(person_folder)
            print(f"Folder created at '{person_folder}'.")
        else:
            print("Folder not created. Exiting.")
            exit()
    return person_folder

def scrape_medical_report(file_path):
    try:
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            medical_data = {}
            
            # Health-related keywords for disease prediction
            health_keywords = [
                "glucose", "cholesterol", "triglycerides", "hemoglobin", "creatinine", "urea", 
                "uric acid", "ast", "alt", "ggtp", "alp", "bilirubin", "protein", "albumin", 
                "hdl", "ldl", "vldl", "non-hdl", "gfr", "bun", "a : g", "globulin"
            ]
            
            # Patterns
            value_pattern = r"(\d+\.?\d*)"
            test_section = False
            current_test = ""
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Skip metadata and headers
                if any(kw in line_lower for kw in ["name", "lab no", "ref by", "collected", "reported", 
                                                   "a/c status", "processed at", "test name", "units", 
                                                   "bio. ref", "note", "customer care", "tel", "page"]):
                    continue
                
                # Start of test section
                if any(kw in line_lower for kw in ["liver", "kidney", "lipid", "serum"]):
                    test_section = True
                    continue
                
                if not test_section:
                    continue
                
                # Identify test name (no numbers, followed by a value)
                if not re.search(r"\d", line) and any(kw in line_lower for kw in health_keywords):
                    current_test = line.strip()
                    continue
                
                # Extract value if it’s a number
                value_match = re.search(value_pattern, line)
                if value_match and current_test:
                    value = float(value_match.group(1))
                    # Clean test name
                    test_key = re.sub(r"[^\w]", "_", current_test.lower().split("(")[0].strip())[:25]
                    if "ratio" in test_key and "bun" in test_key:
                        test_key = "bun_creatinine_ratio"
                    elif "cholesterol" in test_key and "total" not in test_key:
                        test_key = f"{test_key}_cholesterol"
                    medical_data[test_key] = value
                    current_test = ""
            
            return medical_data if medical_data else None
            
    except Exception as e:
        print(f"Error reading report: {e}")
        return None

def save_medical_data(person_folder, person_name, person_id, medical_data):
    medical_file = os.path.join(person_folder, f"medical_{person_name}_{person_id}.xlsx")
    if medical_data:
        df_vertical = pd.DataFrame({
            "Parameter": list(medical_data.keys()),
            "Value": list(medical_data.values())
        })
        
        if os.path.exists(medical_file):
            existing_data = pd.read_excel(medical_file)
            updated_data = pd.concat([existing_data, df_vertical], ignore_index=True)
        else:
            updated_data = df_vertical
        
        updated_data.to_excel(medical_file, index=False)
        print(f"Medical data saved vertically to '{medical_file}'.")
    else:
        print("No disease-relevant data extracted from report. Nothing saved.")

def main():
    person = login()
    person_id = person["Person ID"]
    person_name = person["Name"]
    person_folder = check_or_create_folder(person_id, person_name)
    report_path = input("Enter the full path to your Dr. Lal Path Lab report file (e.g., S:\\btp\\dr lal path\\format.pdf): ").strip()
    if os.path.exists(report_path):
        medical_data = scrape_medical_report(report_path)
        save_medical_data(person_folder, person_name, person_id, medical_data)
    else:
        print("Report file not found. Please check the path and try again.")

if __name__ == "__main__":
    main()