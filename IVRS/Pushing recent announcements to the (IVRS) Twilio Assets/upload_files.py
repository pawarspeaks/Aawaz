from twilio.rest import Client
import os


# List of file names
file_names = [
    "Dindigul_marathi.mp3",
    "Dindigul_english.mp3",
    "Dindigul_tamil.mp3",
    "Dindigul_french.mp3",
    "Dindigul_german.mp3",
    "Dindigul_hindi.mp3",
]

# Create a Twilio client object
# client = Client(account_sid, auth_token)

# Get the current script's directory
script_directory = os.path.dirname(os.path.realpath(__file__))
static_directory = os.path.join(script_directory, "static")

# Loop through each file and upload
for file_name in file_names:
    full_path = os.path.join(static_directory, file_name)

    if not os.path.exists(full_path):
        print(f"Error with file'{file_name}'not pushed/uploaded to assets")
        continue

    # Open file in binary mode
    with open(full_path, "rb") as file:
        # Upload the file and print the URL
        media = client.proxy.services("your_service_sid").assets.create(media_data=file.read())
        print(f"Uploaded file: {file_name}, URL: {media.sid}")

print("All files uploaded successfully!")
