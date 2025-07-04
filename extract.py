from faker import Faker
from google.cloud import storage
import csv

# Initialize Faker
fake = Faker()

# Parameters
num_records = 100
csv_file = "dummy_employee_data.csv"
bucket_name = "fp_employee_bucket"  # 🔁 Replace with your bucket
destination_blob_name = "dummy_employee_data.csv"  # GCS path
gcp_key_path = "/Users/harshashetty/Desktop/GCP First Project/my-service-account-key.json" # 🔁 Replace with your service account key path

# Fields for CSV
fields = [
    "EmployeeID",
    "FullName",
    "Email",
    "Password",
    "PhoneNumber",
    "SSN",
    "DateOfBirth",
    "Address",
    "JobTitle",
    "Department",
    "StartDate",
    "Salary"
]

# Function to generate a dummy employee record
def generate_employee(employee_id):
    return {
        "EmployeeID": employee_id,
        "FullName": fake.name(),
        "Email": fake.email(),
        "Password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
        "PhoneNumber": fake.phone_number(),
        "SSN": fake.ssn(),
        "DateOfBirth": fake.date_of_birth(minimum_age=22, maximum_age=60).strftime("%Y-%m-%d"),
        "Address": fake.address().replace("\n", ", "),
        "JobTitle": fake.job(),
        "Department": fake.random_element(elements=("Engineering", "HR", "Sales", "Marketing", "Finance")),
        "StartDate": fake.date_between(start_date='-10y', end_date='today').strftime("%Y-%m-%d"),
        "Salary": fake.random_int(min=50000, max=150000)
    }

# Write to CSV
print("📄 Writing employee data to CSV...")
with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for i in range(1, num_records + 1):
        writer.writerow(generate_employee(i))

print(f"✅ CSV file created: {csv_file}")

# Upload to GCS
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name, key_path):
    print("☁️  Uploading to Google Cloud Storage...")
    try:
        client = storage.Client.from_service_account_json(key_path)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)
        print(f"✅ File uploaded to: gs://{bucket_name}/{destination_blob_name}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

# Trigger the upload
upload_to_gcs(bucket_name, csv_file, destination_blob_name, gcp_key_path)
