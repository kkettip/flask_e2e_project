import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from faker import Faker
import random

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

# Create a database engine
db_engine = create_engine(conn_string, echo=False)
fake = Faker()

sample_conditions = ['cough', 'allergies', 'rash', 'flu', 'covid', 
                      'headache', 'sore_throat', 'fever', 
                      'stomach_ache', 'diarrhea']

def insert_fake_data(engine, num_patients=100, num_conditions=20, num_patient_conditions=150): # Noqa: E501
    # Start a connection
    with engine.connect() as connection:
        # Insert fake data into patients
        for _ in range(num_patients):
            first_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(minimum_age=10, maximum_age=90)
            connection.execute(f"INSERT INTO patients (first_name, last_name, date_of_birth) VALUES ('{first_name}', '{last_name}', '{date_of_birth}')") # Noqa: E501

        # Insert sample conditions into conditions
        for condition in sample_conditions:
            connection.execute(f"INSERT INTO conditions (condition_name) VALUES ('{condition}')") # Noqa: E501
        
        # Fetch all patient IDs and condition IDs
        patient_ids = [row[0] for row in connection.execute("SELECT patient_id FROM patients").fetchall()] # Noqa: E501
        condition_ids = [row[0] for row in connection.execute("SELECT condition_id FROM conditions").fetchall()] # Noqa: E501
        
        # Insert fake data into patient_conditions
        for _ in range(num_patient_conditions):
            patient_id = random.choice(patient_ids)
            condition_id = random.choice(condition_ids)
            intake_date = fake.date_between(start_date="-5y", end_date="today")
            connection.execute(f"""INSERT INTO patient_conditions (patient_id, condition_id, intake_date) VALUES ({patient_id}, {condition_id}, '{intake_date}')""") # Noqa: E501

if __name__ == "__main__":
    insert_fake_data(db_engine)
    print("Fake data insertion complete!")