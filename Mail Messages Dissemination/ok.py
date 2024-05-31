import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(to_email, subject, body, language, audio_file_path):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "odop662@gmail.com"  # Replace with your Gmail email
    smtp_password = "ucns nwym ssqk qvom"  # Replace with your Gmail password

    # Create the email message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # Attach audio file based on language
    attach_audio(message, audio_file_path)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

def attach_audio(message, audio_file_path):
    # Attach the audio file
    audio_attachment = open(audio_file_path, 'rb')
    audio_base = MIMEBase('application', 'octet-stream')
    audio_base.set_payload(audio_attachment.read())
    encoders.encode_base64(audio_base)
    audio_base.add_header('Content-Disposition', 'attachment; filename="audio.mp3"')
    message.attach(audio_base)

# Read data from CSV file
csv_file_path = r'C:\Users\Asus\Downloads\SIH2023\SIH2023\user_data_with_email.csv'

with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    dataset = list(reader)

# Send emails
for user_data in dataset:
    name = user_data['Name']
    email = user_data['Email ID']
    pnr_status = user_data['PNR Status']
    train_location = user_data['Train Location']
    station_name = user_data['Station Name']
    ticket_cancellation = user_data['Ticket Cancellation']
    language = user_data['Language']

    subject = f"Train Journey Information - {name}"

    # Language-specific messages
    if language == 'Hindi':
        body = f"Dear {name},\n\nआपकी ट्रेन यात्रा का विवरण निम्नलिखित है:\n\nट्रेन संख्या: {pnr_status}\nट्रेन का नाम: {train_location}\nस्थान: {station_name}\nटिकट रद्द करना: {ticket_cancellation}\n\nधन्यवाद,\nभारतीय रेलवे\n for IVRS  +12058904794"
        audio_file_path = 'C:\\Users\\Asus\\Downloads\\SIH2023\\SIH2023\\Dindigul_hindi.mp3'
    elif language == 'Tamil':
        body = f"Dear {name},\n\nஉங்கள் இருந்து விருந்தினர் விவரங்கள் பின்வரும் உள்ளன:\n\nரயில் எண்: {pnr_status}\nரயிலின் பெயர்: {train_location}\nநிலையம்: {station_name}\nடிக்கெட் ரத்து: {ticket_cancellation}\n\nவாழ்த்துக்கள்,\nஇந்திய ரயில்வே\n for IVRS  +12058904794"
        audio_file_path = 'C:\\Users\\Asus\\Downloads\\SIH2023\\SIH2023\\Dindigul_tamil.mp3'
    elif language == 'Marathi':
        body = f"Dear {name},\n\nतुमच्या रेल्वे यात्रेची माहिती खालीलप्रमाणे आहे:\n\nरेल्वे क्रमांक: {pnr_status}\nरेल्वे नाव: {train_location}\nस्थान: {station_name}\nटिकट रद्द करणे: {ticket_cancellation}\n\nआभार,\nभारतीय रेल्वे\n for IVRS  +12058904794"
        audio_file_path = 'C:\\Users\\Asus\\Downloads\\SIH2023\\SIH2023\\Dindigul_marathi.mp3'
    else:
        # Default to English
        body = f"Dear {name},\n\nYour train journey details are as follows:\n\nTrain No: {pnr_status}\nTrain Name: {train_location}\nStation: {station_name}\nTicket Cancellation: {ticket_cancellation}\n\nRegards,\nIndian Railways\n for IVRS  +12058904794"
        audio_file_path = 'C:\\Users\\Asus\\Downloads\\SIH2023\\SIH2023\\Dindigul_english.mp3'

    send_email(email, subject, body, language, audio_file_path)

print("Emails sent successfully!")
