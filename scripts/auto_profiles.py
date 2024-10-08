import csv
import random
import hashlib
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Sample data lists for relevant columns
makes_and_models = [
    ('Honda', 'Accord', 'Sedan', 'HON', 'EX'),
    ('Toyota', 'RAV4', 'SUV', 'TOY', 'LE'),
    ('Volkswagen', 'Jetta', 'Sedan', 'VW', 'S'),
    ('Toyota', 'Camry', 'Sedan', 'TOY', 'XLE')
]
fuel_types = ['G', 'D', 'H']
mileage_options = ['5K', '10K', '15K', '25K', '35K']
vin_prefixes = ['1HGCM', '2T3ZF', '3VW5T', '4T1BF']

# Function to generate a valid VIN
def generate_vin():
    return random.choice(vin_prefixes) + ''.join(random.choices('0123456789ABCDEFGHJKLMNPRSTUVWXYZ', k=11))

# Function to generate a random email hash
def generate_email_md5():
    email = fake.email()
    return hashlib.md5(email.encode()).hexdigest()

# Function to read email MD5s from a file
def read_md5s_from_file(file_path):
    df = pd.read_csv(file_path)
    return df['EMAIL_MD5'].tolist()

# Function to add months to a date
def add_months(start_date, months):
    new_month = start_date.month - 1 + months
    year = start_date.year + new_month // 12
    month = new_month % 12 + 1
    day = min(start_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return start_date.replace(year=year, month=month, day=day)

# Function to generate rows
def generate_auto_profiles_data(num_records, md5_list):
    data = []
    for _ in range(num_records):
        make, model, veh_class, mfgcd, stylecd = random.choice(makes_and_models)
        year = str(random.randint(2018, 2023))
        fuel_type = random.choice(fuel_types)
        mileage = random.choice(mileage_options)
        nbr_vehicles = str(random.randint(1, 3))
        idate = fake.date_between(start_date='-2y', end_date='today')
        odate = add_months(idate, 6)  # Add 6 months to IDATE
        vin = generate_vin()
        email_md5 = random.choice(md5_list)

        row = [vin, make, model, year, veh_class, fuel_type, mfgcd, stylecd, mileage, nbr_vehicles, idate.strftime('%Y-%m-%d'), odate.strftime('%Y-%m-%d'), email_md5]
        data.append(row)

    return data

# Write data to CSV file
def write_to_csv(filename, num_records):
    fieldnames = ['VIN', 'MAKE', 'MODEL', 'YEAR', 'VEH_CLASS', 'FUELTYPECD', 'MFGCD', 'STYLECD', 'MILEAGECD', 'NBRVEHICLES', 'IDATE', 'ODATE', 'EMAIL_MD5']
    md5_list = read_md5s_from_file('demo_md5s.csv')
    data = generate_auto_profiles_data(num_records, md5_list)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(data)

    print(f"{num_records} records written to {filename}")

# Generate 100 records and save to CSV
if __name__ == "__main__":
    num_records = int(input("Enter the number of records to generate: "))
    write_to_csv("auto_profiles_data.csv", num_records)