import pandas as pd
import csv
import json
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

SITE_ID = 'zeta-retail'
ACCOUNT_KEY = 1000
ACCOUNT_NAME = 'Zeta Retail Account'

# Read BSIN and Email from unique_records.csv

def read_unique_records_in_batches(file_path, chunk_size):
    """Reads the unique_records.csv file in chunks and returns only BSIN and EMAIL columns."""
    for chunk in pd.read_csv(file_path, usecols=['BSIN', 'EMAIL'], chunksize=chunk_size):
        yield chunk.values.tolist()  # Return as list of lists for each chunk


# Function to generate random timestamp in the last 4 months
def random_timestamp(start_date, end_date):
    return start_date + timedelta(seconds=random.randint(0, int((end_date- start_date).total_seconds())))

# Function to generate random properties
def generate_properties(common_values, record_timestamp):
    return {
        "attribution_model": common_values["attribution_model"],
        "campaign_id": common_values["campaign_id"],
        "campaign_name": common_values["campaign_name"],
        "campaign_segments": common_values["campaign_segments"],
        "campaign_tags": common_values["campaign_tags"],
        "campaign_tracking_codes": common_values["campaign_tracking_codes"],
        "campaign_type": common_values["campaign_type"],
        "channel": random.choice(["Email", "SMS"]),
        "contact_type": random.choice(["Email", "PhoneNumber"]),
        "contact_value": fake.email(),
        "conversion_value": round(random.uniform(10, 100), 2),
        "converting_event": {
            "event": "purchased",
            "store": random.randint(1, 1000),
            "properties": {
                "doc_referrer": fake.url(),
                "href": fake.url(),
                "last_purchase": {
                    "datafields": {
                        "cartsubtotal": round(random.uniform(20, 200), 2),
                        "carttotal": round(random.uniform(20, 200), 2),
                        "discount": round(random.uniform(1, 50), 2),
                        "ordernumber": str(random.randint(100000000000, 999999999999)),
                        "ordertax": round(random.uniform(1, 20), 2),
                    },
                    "items": [
                        {
                            "color": fake.color_name(),
                            "id": str(random.randint(1000000, 9999999)),
                            "price": round(random.uniform(10, 100), 2),
                            "quantity": random.randint(1, 5),
                            "resourcetype": "product",
                            "size": random.choice(["S", "M", "L", "XL"]),
                            "sku": fake.ean8()
                        }
                    ],
                    "total": round(random.uniform(20, 200), 2)
                },
                "resource_id": str(uuid.uuid4()),
                "session": str(uuid.uuid4())
            },
            "received_timestamp": record_timestamp.utcnow().isoformat(),
            "site_id": common_values["site_id"],
            "timestamp": record_timestamp.utcnow().isoformat()
        },
        "dispatched_at": record_timestamp.utcnow().isoformat(),
        "email_from": fake.email(),
        "is_seed": False,
        "is_transactional": False,
        "launch_type": "scheduled",
        "message_time": record_timestamp.utcnow().isoformat(),
        "message_uid": str(uuid.uuid4()),
        "nudge_token": str(uuid.uuid4()),
        "parent_recurrence_index": "1",
        "preheader_text": common_values["preheader_text"],
        "publish_event_timestamp": record_timestamp.utcnow().isoformat(),
        "recurrence_index": "1",
        "subject_line": common_values["subject_line"],
        "targeted_segment_id": common_values["targeted_segment_id"],
        "targeted_segment_name": common_values["targeted_segment_name"],
        "targeted_segment_priority": common_values["targeted_segment_priority"],
        "template_id": common_values["template_id"],
        "template_preheader_text": common_values["template_preheader_text"],
        "template_subject": common_values["template_subject"],
        "variation_sent": "A",
        "variation_testing_enabled": True,
        "version_campaign_id": common_values["version_campaign_id"],
        "version_name": common_values["version_name"],
        "version_token": common_values["version_token"]
    }

# Function to generate common values for the campaign
def generate_common_campaign_values():
    campaign_names = ["Welcome", "Promotion", "Deals", "Holiday Sale", "Clearance", "Black Friday", "Cyber Monday",
                  "Back to School", "Loyalty Program", "Referral", "Birthday Offer", "Free Shipping", "Flash Sale",
                  "Summer Sale", "Winter Discounts", "VIP Offer", "Bundle Deals", "BOGO", "Limited Time", "Exclusive"]

    # Generate discount rate and current day of the week
    discount_rate = random.randint(10, 50)
    day_of_week = datetime.utcnow().strftime('%A')  # Get the current day of the week

    # Generate a relevant campaign name
    campaign_name = f"{random.choice(campaign_names)} - {discount_rate}% off on {day_of_week}"

    return {
        "attribution_model": "last_click",
        "campaign_id": random.randint(1000000, 9999999),
        "campaign_name": campaign_name,
        "campaign_segments": [random.randint(100000, 200000), random.randint(200000, 300000)],
        "campaign_tags": ["Deal"],
        "campaign_tracking_codes": {
            "utm_campaign": f"{campaign_name}-variant-A",
            "utm_medium": "email",
            "utm_source": "zeta"
        },
        "campaign_type": "manual",
        "preheader_text": "Shop the Deals & get FREE shipping through tomorrow!",
        "site_id": SITE_ID,
        "subject_line": f"Shop big, save big! {discount_rate}% off $199",
        "targeted_segment_id": random.randint(100000, 200000),
        "targeted_segment_name": "*Engaged 30 Days",
        "targeted_segment_priority": 1,
        "template_id": random.randint(1000000, 2000000),
        "template_preheader_text": "Shop the Deals & get FREE shipping through tomorrow!",
        "template_subject": f"Shop big, save big! {discount_rate}% off $199",
        "version_campaign_id": random.randint(1000000, 9999999),
        "version_name": f"{campaign_name}_v{random.randint(1,5)}",
        "version_token": str(uuid.uuid4())
    }

# Function to generate sample 'v' field using valid random values
def generate_v(bsin, email, record_timestamp):
    return {
        "bsin": bsin,
        "enriched": {
            "geolocation": fake.location_on_land(),
            "http_method": fake.http_method(),
            "is_bot": fake.boolean(),
            "referer": fake.url(),
            "user_agent": fake.user_agent(),
            "user_agent_detail": fake.user_agent()
        },
        "event_id": str(uuid.uuid4()),
        "event_type": "system::message_delivered",
        "identified": fake.boolean(),
        "identity": {
            "attributes": [],
            "bsin": bsin,
            "email": email,
            "scoped_attributes": {},
            "user_id": fake.uuid4()
        },
        "is_test": False,
        "metadata": {
            "process_hostname": "event-service-processor-o",
            "process_id": str(uuid.uuid4()),
            "process_timestamp": record_timestamp.utcnow().isoformat(),
            "receive_hostname": "kt-event-service-e",
            "receive_id": str(uuid.uuid4()),
            "receive_timestamp": record_timestamp.utcnow().isoformat()
        },
        "property_format": "JSON",
        "resource_id": str(uuid.uuid4()),
        "resource_type": "product",
        "site_id": SITE_ID,
        "source_event_id": str(uuid.uuid4()),
        "status": "PROCESSED",
        "timestamp": record_timestamp.utcnow().isoformat(),
        "url": fake.url()
    }

# Function to generate data
def generate_data(num_records, unique_records_list):
    data = []

    start_date = datetime.now() - timedelta(days=120)
    end_date = datetime.now()

    records_in_current_campaign = random.randint(20000, 50000)  # Random number of records per campaign
    common_values = generate_common_campaign_values()

    for i in range(num_records):
        if i % records_in_current_campaign == 0:
            common_values = generate_common_campaign_values()  # Change campaign details after random 20K-50K records
            records_in_current_campaign = random.randint(20000, 50000)

        bsin, email = random.choice(unique_records_list)
        record_timestamp = random_timestamp(start_date, end_date)
        v_field = generate_v(bsin, email, record_timestamp)  # Generate the 'v' field with random values

        record = {
            "EVENT_ID": str(uuid.uuid4()),
            "EVENT_TYPE": "email_sent",
            "SITE_ID": common_values["site_id"],
            "BSIN": bsin,
            "EMAIL": email,
            "USER_ID": fake.uuid4(),
            "PROPERTIES": json.dumps(generate_properties(common_values, record_timestamp)),
            "DT": record_timestamp.isoformat(),
            "V": json.dumps(v_field),  # Use the generated 'v' field here
            "ETL_TIME": record_timestamp.utcnow().isoformat()
        }
        data.append(record)

    return data

# Write the data to a CSV file
def write_csv(filename, num_records, batch_size=25000, unique_records_file='unique_records.csv', chunk_size=25000):
    header = [
        "EVENT_ID", "EVENT_TYPE", "SITE_ID", "BSIN", "EMAIL", "USER_ID",
        "PROPERTIES", "DT", "V", "ETL_TIME"
    ]

    total_records_written = 0

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Read unique_records.csv in chunks
        for unique_records_chunk in read_unique_records_in_batches(unique_records_file, chunk_size):
            # While we still have records to generate
            while total_records_written < num_records:

                # Ensure we don't exceed the total required records
                batch_size_to_write = min(batch_size, num_records - total_records_written)

                # Generate data for the current batch
                generated_data = generate_data(batch_size_to_write, unique_records_chunk)

                # Write the batch to the CSV
                writer.writerows(generated_data)
                total_records_written += batch_size_to_write

                # Print message after writing each batch
                print(f"{batch_size_to_write} records written. Total so far: {total_records_written}/{num_records}")

                # If we've written enough records, break out of the loop
                if total_records_written >= num_records:
                    break

if __name__ == "__main__":
    num_records = int(input("Enter the number of records to generate: "))
    file_name = "retail_events_v.csv"
    write_csv(file_name, num_records)
    print(f"{num_records} records have been written to {file_name}")