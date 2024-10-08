from google.cloud import bigquery
from faker import Faker
import pandas as pd
import os
import time
import json
from google.api_core.exceptions import ServiceUnavailable

# Set up BigQuery client
def connect_to_bigquery(json_key_path, project_id):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_key_path
    client = bigquery.Client(project=project_id)
    return client

# Function to read email and email_md5 from combined_data.csv
def read_email_data(file_path):
    df = pd.read_csv(file_path)

    if 'email_md5' not in df.columns or 'email' not in df.columns:
        raise KeyError("The required columns 'email_md5' and 'email' are not present in the CSV file.")

    return df[['email_md5', 'email']].to_dict('records')

# Function to generate fake data using Faker and merge with email data
def generate_policy_holder_data(n, email_data):
    fake = Faker()
    data = []

    for i in range(n):
        email_record = email_data[i % len(email_data)]  # Cycle through the email records if n > len(email_data)

        data.append({
            "policy_holder_id": fake.uuid4(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "gender": fake.random_element(elements=('Male', 'Female', 'Other')),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=90),
            "ssn": fake.ssn(),
            "phone_number": fake.phone_number(),
            "email": email_record['email'],  # Use email from file
            "email_md5": email_record['email_md5'],  # Use email_md5 from file
            "address_line1": fake.street_address(),
            "address_line2": fake.secondary_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.postcode(),
            "country": fake.country(),
            "driver_license_number": str(fake.random_number(digits=8)),  # Convert to string
            "driver_license_state": fake.state_abbr(),
            "vehicle_identification_number": fake.unique.random_number(digits=17),
            "policy_number": fake.uuid4(),
            "policy_start_date": fake.date_this_decade(),
            "policy_end_date": fake.date_this_decade(),
            "policy_type": fake.random_element(elements=('Comprehensive', 'Third-party')),
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year(),
        })

    df = pd.DataFrame(data)
    df['driver_license_number'] = df['driver_license_number'].astype(str)  # Ensure dtype is string
    df['vehicle_identification_number'] = df['vehicle_identification_number'].astype(str)  # Convert VIN to string
    return df

# Function to upload data to BigQuery with retry mechanism
def upload_to_bigquery(df, client, dataset_id, table_id, max_retries=5):
    table_ref = f"{client.project}.{dataset_id}.{table_id}"
    attempt = 0
    while attempt < max_retries:
        try:
            job = client.load_table_from_dataframe(df, table_ref)
            job.result()  # Wait for the job to complete
            print(f"{len(df)} records have been inserted into {table_ref}")
            break
        except ServiceUnavailable as e:
            attempt += 1
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Service unavailable. Retrying in {wait_time} seconds... (Attempt {attempt}/{max_retries})")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Failed to insert data: {e}")
            break

# Function to save the DataFrame to a CSV file
def save_to_csv(df, file_name):
    df.to_csv(file_name, index=False)
    print(f"Data has been saved to {file_name}")

# Main function to generate, save, and load data
def main():
    json_key_path = 'bq_connection.json'  # Update this with your JSON key file path
    project_id = 'gcpaccount'  # Project ID
    dataset_id = 'etl'  # Dataset where your table resides
    table_id = 'policy_holder_info'  # Table name
    csv_file_name = 'policy_holder_data.csv'  # Output CSV file name
    combined_file_path = 'combined_data.csv'  # Path to combined data

    # Connect to BigQuery
    client = connect_to_bigquery(json_key_path, project_id)

    # Read email and email_md5 data from CSV
    email_data = read_email_data(combined_file_path)

    # Number of records to generate
    num_records = int(input("Enter the number of records to generate: "))

    # Generate fake data
    df = generate_policy_holder_data(num_records, email_data)

    # Save data to CSV
    save_to_csv(df, csv_file_name)

    # Upload data to BigQuery
    upload_to_bigquery(df, client, dataset_id, table_id)

if __name__ == "__main__":
    main()