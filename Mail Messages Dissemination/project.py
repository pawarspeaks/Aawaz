import csv
import random

# Provided user data with email IDs
user_data = [
    ["Chhavi Mohitkar", "chhavi.mohitkar2021@vitbhopal.ac.in"],
    ["Aditya Mohite", "mohite.uttamrao2021@vitbhopal.ac.in"],
    ["Pratap Pawar", "pratappawar.dnyandeo2021@vitbhopal.ac.in"],
    ["Atharva", "atharva2021@vitbhopal.ac.in"],
    ["Gayatri", "gayatri.mistary2021@vitbhopal.ac.in"],
    ["Pranav", "pranav2021@vitbhopal.ac.in"]
]

# Generate random values for PNR Status, Train Location, and Ticket Cancellation
random_data = []
for user in user_data:
    name = user[0]
    email_id = user[1]
    pnr_status = f"PNR_{random.randint(1000000000, 9999999999)}"
    train_location = f"{random.choice(['Kolkata Exp', 'Chennai Exp', 'Mumbai Exp', 'Delhi Exp'])}"
    station_name = f"Station_{random.randint(1, 10)}"
    ticket_cancellation = random.choice([True, False])
    random_data.append([name, email_id, pnr_status, train_location, station_name, ticket_cancellation])

# CSV file path
csv_file_path = "user_data_with_email.csv"

# Write the data to the CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email ID", "PNR Status", "Train Location", "Station Name", "Ticket Cancellation"])
    writer.writerows(random_data)

print(f"CSV file with random data (including email IDs) has been created: {csv_file_path}")
