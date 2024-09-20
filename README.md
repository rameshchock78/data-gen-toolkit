Here’s the `README.md` content and folder structure formatted for easy copy-pasting into GitHub:

### Folder Structure
```
data-gen-toolkit/
│
├── README.md
├── requirements.txt
│
├── config/
    ├── bq_connection.json
├── scripts/
│   ├── unique_ids.py
│   ├── retail_events.py
│   ├── user_props.py
│   ├── policy_holder_info.py
│   ├── demographics.py
│   ├── location.py
│   ├── auto_profiles.py
│
└── data/
    ├── unique_ids.csv
    └── generated_data/
```

# Data Generation Toolkit

The `data-gen-toolkit` is a Python-based data generation tool designed to create synthetic datasets with a common key structure. This toolkit is useful for generating test data for retail events, user profiles, policy holders, demographics, locations, and auto profiles. Each dataset contains a set of shared keys (BSIN, email, email_md5) to enable easy joining across different tables.

## Key Features

- **Unique Record Generation**: The `unique_records.py` script generates a unique combination of BSIN, email, and email_md5, which are used across all datasets.
- **Customizable Data**: Modify scripts to generate specific fields and formats for each dataset.
- **Easy Integration**: The shared keys allow easy joining of datasets for more comprehensive testing scenarios.

## Folder Structure

- **scripts/**: Contains all data generation scripts.
- **data/**: Stores generated CSV files, with a separate folder for unique records and generated data.

## Dependencies

To install the required Python dependencies, run:

```bash
pip install -r requirements.txt
```

## Folder Structure

- **scripts/**: Contains all data generation scripts.
- **data/**: Stores generated CSV files, with a separate folder for unique records and generated data.

## Dependencies

To install the required Python dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

1. **Generate Unique Records**:
   Run the `unique_ids.py` script to generate the BSIN, email, and email_md5 combination:

   ```bash
   python scripts/unique_ids.py
   ```

   This will generate a CSV file `unique_ids.csv` in the `data/` folder.

2. **Generate Dataset Specific Data**:
   Each of the scripts depends on `unique_ids.csv` to populate the shared keys.

   - To generate retail event data:

     ```bash
     python scripts/retail_events.py
     ```

   - To generate user properties data:

     ```bash
     python scripts/user_props.py
     ```

   - To generate policy holder information:

     ```bash
     python scripts/policy_holder_info.py
     ```

   - To generate demographics data:

     ```bash
     python scripts/demographics.py
     ```

   - To generate location data:

     ```bash
     python scripts/location.py
     ```

   - To generate auto profile data:

     ```bash
     python scripts/auto_profiles.py
     ```

   Each script will save its output as a CSV file in the `data/generated_data/` folder.

## Example

You can run all scripts in sequence to generate data with consistent keys across all datasets:

```bash
python scripts/unique_ids.py
python scripts/retail_events.py
python scripts/user_props.py
python scripts/policy_holder_info.py
python scripts/demographics.py
python scripts/location.py
python scripts/auto_profiles.py
```

### `requirements.txt`

```
pandas
faker
google-cloud-bigquery
uuid
boto3
random
hashlib
```

This version is optimized for direct copy-pasting into the GitHub editor without needing any extra formatting adjustments.
