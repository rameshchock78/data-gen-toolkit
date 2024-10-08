import csv
import uuid
import hashlib
from faker import Faker

# Initialize Faker
fake = Faker()

# Function to generate MD5 hash from an email
def generate_md5(email):
    return hashlib.md5(email.encode()).hexdigest()

# Function to generate a unique record
def generate_record():
    email = fake.unique.email()
    email_md5 = generate_md5(email)
    bsin = str(uuid.uuid4())
    return bsin, email_md5, email

# Generate records and save them to a CSV
def generate_unique_records(num_records, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['BSIN', 'EMAIL_MD5', 'EMAIL'])

        for _ in range(num_records):
            record = generate_record()
            writer.writerow(record)

# Number of records to generate (input can be dynamic)
num_records = int(input("Enter the number of records to generate: "))
output_file = 'unique_records.csv'

# Generate and save records
generate_unique_records(num_records, output_file)

print(f"{num_records} unique records have been generated and saved to '{output_file}'.")