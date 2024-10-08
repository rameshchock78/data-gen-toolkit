import csv
import pandas as pd
import json
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta
from decimal import Decimal

# Function to convert Decimal to float
def convert_decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal_to_float(i) for i in obj]
    else:
        return obj

# Function to generate random timestamp
def random_timestamp(start_date, end_date):
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Function to generate random data for the properties column
def generate_properties():
    fake = Faker()
    return {
        "a1_street_address": fake.street_address(),
        "a2_city": fake.city(),
        "a3_state": fake.state_abbr(),
        "a4_postal_code": fake.postcode(),
        "a5_country": fake.country_code(),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "bsin": str(uuid.uuid4()),
        "created_at": fake.date_time_this_decade().isoformat(),
        "engagement_site": {
            "touch_dt": fake.date_time_this_decade().isoformat(),
            "value": random.randint(1, 100)
        },
        "engagement_site_visit": {
            "touch_dt": fake.date_time_this_decade().isoformat(),
            "value": random.randint(1, 100)
        },
        "first_name": fake.first_name(),
        "has_active_email": str(random.choice([True, False])).lower(),
        "has_active_phone": str(random.choice([True, False])).lower(),
        "has_active_push_device": str(random.choice([True, False])).lower(),
        "has_active_subscription": str(random.choice([True, False])).lower(),
        "known_to_customer": random.choice([True, False]),
        "known_to_zeta": random.choice([True, False]),
        "last_seen": fake.date_time_this_decade().isoformat(),
        "last_updated": fake.date_time_this_decade().isoformat(),
        "name": fake.name(),
        "ns_browser": fake.user_agent(),
        "ns_city": fake.city(),
        "ns_country": fake.country_code(),
        "ns_device_type": fake.word(),
        "ns_latitude": convert_decimal_to_float(fake.latitude()),  # Convert if needed
        "ns_longitude": convert_decimal_to_float(fake.longitude()),  # Convert if needed
        "ns_metro_code": random.randint(100, 999),
        "ns_operating_system": fake.word(),
        "ns_postal_code": fake.postcode(),
        "ns_region": fake.state_abbr(),
        "ns_timezone": fake.timezone(),
        "session_history": [
            {
                "engagement_site": random.randint(1, 10),
                "engagement_site_visit": random.randint(1, 10),
                "session_id": str(uuid.uuid4()),
                "touch_dt": fake.date_time_this_decade().isoformat()
            }
        ],
        "signed_up_at": fake.date_time_this_decade().isoformat(),
        "top_products": {
            "first": fake.word(),
            "touch_dt": fake.date_time_this_decade().isoformat()
        },
        "z_city": fake.city(),
        "z_country": fake.country_code(),
        "z_latitude": convert_decimal_to_float(fake.latitude()),  # Convert if needed
        "z_longitude": convert_decimal_to_float(fake.longitude()),  # Convert if needed
        "z_state": fake.state_abbr(),
        "z_zip": fake.postcode()
    }

# Read BSIN, EMAIL, and EMAIL_MD5 from existing CSV file
def read_combined_data(file_path):
    df = pd.read_csv(file_path)
    return df[['BSIN', 'EMAIL', 'EMAIL_MD5']]

def generate_data_from_combined(num_records, combined_df):
    fake = Faker()
    data = []

    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)

    for _, row in combined_df.head(num_records).iterrows():
        record = {
            "BSIN": row['BSIN'],
            "USER_ID": fake.uuid4(),
            "EMAIL": row['EMAIL'],
            "CONTACTS": json.dumps({"email": row['EMAIL']}),
            "PROPERTIES": json.dumps(convert_decimal_to_float(generate_properties())),  # Convert if needed
            "LAST_UPDATED": random_timestamp(start_date, end_date).isoformat(),
            "SITE_ID": fake.word(),
            "REPLACED_BY": fake.uuid4(),
            "EMAIL_MD5": row['EMAIL_MD5'],
            "SUB_SITE_IDS": json.dumps([]),
            "SCOPED_PROPERTIES": json.dumps({}),
            "SCOPED_CONTACTS": json.dumps({}),
            "IMPORTED_FROM": json.dumps({}),
            "IMPORTED_FROM_ETL_TIME": json.dumps({}),
            "MERGED_BSINS": json.dumps([]),
            "CONSENT": json.dumps({}),
            "EXTERNAL_IDS": json.dumps({}),
            "UNIQUE_CLIENT_IDS": json.dumps({})
        }
        data.append(record)

    return data

def write_csv(filename, num_records):
    header = [
        "BSIN", "USER_ID", "EMAIL", "CONTACTS", "PROPERTIES", "LAST_UPDATED",
        "SITE_ID", "REPLACED_BY", "EMAIL_MD5", "SUB_SITE_IDS", "SCOPED_PROPERTIES",
        "SCOPED_CONTACTS", "IMPORTED_FROM", "IMPORTED_FROM_ETL_TIME", "MERGED_BSINS",
        "CONSENT", "EXTERNAL_IDS", "UNIQUE_CLIENT_IDS"
    ]
    combined_df = read_combined_data('combined_data.csv')
    data = generate_data_from_combined(num_records, combined_df)

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=',')
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    num_records = int(input("Enter the number of records to generate: "))
    file_name = "user_props_data.csv"
    write_csv(file_name, num_records)
    print(f"{num_records} records have been written to {file_name}")