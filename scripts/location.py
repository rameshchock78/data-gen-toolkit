import pandas as pd
import random
import uuid
import csv
from faker import Faker
from datetime import datetime, timedelta

# Function to generate random timestamp and convert to UNIX time
def random_unix_time(start_date, end_date):
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    unix_time = int(random_date.timestamp())
    return random_date.strftime('%Y-%m-%d'), unix_time

# Function to read email MD5s from a file
def read_md5s_from_file(file_path):
    df = pd.read_csv(file_path)
    return df['EMAIL_MD5'].tolist()

# Function to generate random data for the table
def generate_data(num_records, md5_list):
    fake = Faker()
    data = []
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)

    locations = [
        ("Walmart", "Retail"),
        ("McDonald's", "Fast Food"),
        ("Costco", "Wholesale"),
        ("Starbucks", "Cafe"),
        ("Target", "Retail"),
        ("Best Buy", "Electronics")
    ]
    
    for _ in range(num_records):
        visit_date, unix_time = random_unix_time(start_date, end_date)
        min_duration_seconds = random.randint(600, 3600)
        distance = random.randint(1, 15)
        advertising_id = uuid.uuid4().hex[:16]
        location_brand, location_category = random.choice(locations)
        email_md5s = random.sample(md5_list, random.randint(1, 3))

        record = {
            "VISIT_DT": visit_date,
            "UNIX_TIME": unix_time,
            "MIN_DURATION_SECONDS": min_duration_seconds,
            "DISTANCE": distance,
            "ADVERTISING_ID": advertising_id,
            "LOCATION_BRAND": location_brand,
            "LOCATION_CATEGORY": location_category,
            "EMAIL_MD5S": email_md5s
        }
        data.append(record)

    return data

# Write the generated data to a CSV file
def write_csv(filename, num_records):
    header = [
        "VISIT_DT", "UNIX_TIME", "MIN_DURATION_SECONDS", "DISTANCE", 
        "ADVERTISING_ID", "LOCATION_BRAND", "LOCATION_CATEGORY", "EMAIL_MD5S"
    ]
    md5_list = read_md5s_from_file('demo_md5s.csv')
    data = generate_data(num_records, md5_list)

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=',')
        writer.writeheader()
        for row in data:
            row['EMAIL_MD5S'] = str(row['EMAIL_MD5S']).replace("'", '"')  # Format as JSON array
            writer.writerow(row)

if __name__ == "__main__":
    num_records = int(input("Enter the number of records to generate: "))
    file_name = "location_data.csv"
    write_csv(file_name, num_records)
    print(f"{num_records} records have been written to {file_name}")
