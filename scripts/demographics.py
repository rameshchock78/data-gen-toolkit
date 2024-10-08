import csv
import random
import hashlib
import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()

# Sample data lists for relevant columns
genders = ['M', 'F']
educations = ['12', '14', '16', '18']  # Simplified education levels
marital_statuses = ['M', 'S']  # M = Married, S = Single
states = ['CA', 'TX', 'NY', 'FL', 'IL']
urbanicity = ['Urban', 'Sub']
races = ['White', 'Black', 'Asian', 'Hispanic']
hispanic_languages = ['Yes', 'No']
income_levels = ['$60K', '$75K', '$90K', '$100K', '$120K']
home_ownerships = ['Own', 'Rent']
presence_of_children = ['Y', 'N']
generations = ['Boomer', 'Gen X', 'Millennial', 'Gen Z']
countries = ['US']
postal_states = ['CA', 'TX', 'NY', 'FL', 'IL']

# Function to generate a random email hash
def generate_email_md5():
    email = fake.email()
    return hashlib.md5(email.encode()).hexdigest()

# Function to read email MD5s from a file
def read_md5s_from_file(file_path):
    df = pd.read_csv(file_path)
    return df['EMAIL_MD5'].tolist()

# Function to generate rows
def generate_demographics_data(num_records, md5_list):
    data = []
    for _ in range(num_records):
        email_md5 = random.choice(md5_list)
        gender = random.choice(genders)
        education = random.choice(educations)
        age = str(random.randint(18, 75))
        marital = random.choice(marital_statuses)
        state = random.choice(states)
        urbanicity_value = random.choice(urbanicity)
        race = random.choice(races)
        hispanic_language = random.choice(hispanic_languages)
        income = random.choice(income_levels)
        home_ownership = random.choice(home_ownerships)
        presence_of_children_value = random.choice(presence_of_children)  # Renamed variable here
        generation = random.choice(generations)
        first_name = fake.first_name()
        last_name = fake.last_name()
        address_line1 = fake.street_address()
        address_line2 = fake.secondary_address()
        city = fake.city()
        postal_state = random.choice(postal_states)
        postal_zip = fake.zipcode()
        country = random.choice(countries)
        num_children = str(random.randint(0, 3))
        children_ages_0_to_3 = random.choice(['Y', 'N'])
        children_ages_4_to_6 = random.choice(['Y', 'N'])
        children_ages_7_to_9 = random.choice(['Y', 'N'])
        children_ages_10_to_12 = random.choice(['Y', 'N'])
        children_ages_13_to_18 = random.choice(['Y', 'N'])

        row = [
            email_md5, gender, education, age, marital, state, urbanicity_value, race,
            hispanic_language, income, home_ownership, presence_of_children_value, generation,
            first_name, last_name, address_line1, address_line2, city, postal_state, postal_zip,
            country, num_children, children_ages_0_to_3, children_ages_4_to_6, children_ages_7_to_9,
            children_ages_10_to_12, children_ages_13_to_18
        ]
        data.append(row)

    return data

# Write data to CSV file
def write_to_csv(filename, num_records):
    fieldnames = [
        'EMAIL_ADDRESS_MD5', 'GENDER', 'EDUC', 'AGE', 'MARITAL', 'STATE', 'URBANICITY',
        'RACE', 'HISPANIC_LANGUAGE', 'INCOME', 'HOME_OWNERSHIP', 'PRESENCE_OF_CHILDREN',
        'GENERATION', 'POSTAL_FIRSTNAME', 'POSTAL_LASTNAME', 'POSTAL_ADDRESSLINE1',
        'POSTAL_ADDRESSLINE2', 'POSTAL_CITY', 'POSTAL_STATE', 'POSTAL_ZIP', 'COUNTRY',
        'NUMBER_OF_CHILDREN', 'CHILDREN_AGES_0_TO_3', 'CHILDREN_AGES_4_TO_6',
        'CHILDREN_AGES_7_TO_9', 'CHILDREN_AGES_10_TO_12', 'CHILDREN_AGES_13_TO_18'
    ]
    md5_list = read_md5s_from_file('demo_md5s.csv')
    data = generate_demographics_data(num_records, md5_list)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(data)

    print(f"{num_records} records written to {filename}")

# Generate 100 records and save to CSV
if __name__ == "__main__":
    num_records = int(input("Enter the number of records to generate: "))
    write_to_csv("demographics_data.csv", num_records)
