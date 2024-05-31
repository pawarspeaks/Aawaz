from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Function to send standard emails
def send_email(to_email, subject, body):
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

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

# Function to send custom emails
def send_custom_email(to_email, subject, body, language, audio_file_path):
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

# Function to attach audio file
def attach_audio(message, audio_file_path):
    audio_attachment = open(audio_file_path, 'rb')
    audio_base = MIMEBase('application', 'octet-stream')
    audio_base.set_payload(audio_attachment.read())
    encoders.encode_base64(audio_base)
    audio_base.add_header('Content-Disposition', 'attachment; filename="audio.mp3"')
    message.attach(audio_base)

# Function to update CSV file with new data
def update_csv(new_data):
    csv_file_path = "user_data_with_email.csv"
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_data)

# Route to upload a new CSV file
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return redirect(request.url)
    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        return redirect(request.url)

    if csv_file:
        csv_file_path = os.path.join('uploads', 'user_data_with_email.csv')
        csv_file.save(csv_file_path)

        # Update the CSV file
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            dataset = list(reader)

        update_csv(dataset)

        return redirect(url_for('send_emails'))

# Route to send standard emails
@app.route('/send_emails')
def send_emails():
    # Read data from the existing CSV file
    csv_file_path = os.path.join('uploads', 'user_data_with_email.csv')
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
            body = f"Dear {name},\n\nअगली ट्रेन प्लेटफॉर्म नंबर 2 पर आएगी।\n\nआपकी ट्रेन यात्रा का विवरण निम्नलिखित है:\n\nट्रेन संख्या: {pnr_status}\nट्रेन का नाम: {train_location}\nस्थान:\nदिंडीगुल जंक्शन \nटिकट रद्द करना: {ticket_cancellation}\n\nधन्यवाद,\nभारतीय रेलवे\n\n for IVRS  +12058904794"
        elif language == 'Tamil':
            body = f"Dear {name},\n\nஅடுத்த ரயில் எந்திருக்கும், மைதான எண் 2-வதுக்கு வருகின்றது\n\nஉங்கள் இருந்து விருந்தினர் விவரங்கள் பின்வரும் உள்ளன:\n\nரயில் எண்: {pnr_status}\nரயிலின் பெயர்: {train_location}\nநிலையம்: \n திண்டுக்கல் ஜங்க்ஷன் \nடிக்கெட் ரத்து: {ticket_cancellation}\n\nவாழ்த்துக்கள்,\nஇந்திய ரயில்வே\n\n for IVRS  +12058904794"
        elif language == 'Marathi':
            body = f"Dear {name},\n\nपुढील ट्रेन प्लॅटफॉर्म क्रमांक 2 वर येईल।\n\nतुमच्या रेल्वे यात्रेची माहिती खालीलप्रमाणे आहे:\n\nरेल्वे क्रमांक: {pnr_status}\nरेल्वे नाव: {train_location}\nस्थान: \n दिंडीगुल जंक्शन\nटिकट रद्द करणे: {ticket_cancellation}\n\nआभार,\nभारतीय रेल्वे\n\n for IVRS  +12058904794"
        else:
            # Default to English
            body = f"Dear {name},\n\nYour train journey details are as follows:\n\nTrain No: {pnr_status}\nTrain Name: {train_location}\nStation: \n Dindigul jn\nTicket Cancellation: {ticket_cancellation}\n\nRegards,\nIndian Railways\n\n for IVRS +12058904794"

        send_email(email, subject, body)

    return "Standard Emails sent successfully!"

# Route to render the form for sending custom emails
@app.route('/send_custom_email_form')
def send_custom_email_form():
    return render_template('send_custom_email.html')

# Route to handle the submission of custom emails
@app.route('/send_custom_email', methods=['POST'])
def send_custom_email():
    to_email = request.form.get('to_email')
    subject = request.form.get('subject')
    body = request.form.get('body')
    language = request.form.get('language')
    audio_file_path = request.form.get('audio_file_path')

    send_custom_email(to_email, subject, body, language, audio_file_path)

    return "Custom Email sent successfully!"

if __name__ == '__main__':
    app.run(debug=True)
