import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

double_beds = ['Double Bed bedroom 1', 'Double Bed bedroom 2', 'Double Bed living room']
single_beds = ['Single Bed 1', 'Single Bed 2']
persons = os.environ.get("PERSONS")

bed_assignments = {}

# assign Katherynne and Chuy to the same bed
if 'Katherynne' in persons and 'Chuy' in persons:
    bed = random.choice(double_beds)
    bed_assignments[bed] = ['Katherynne', 'Chuy']
    persons.remove('Katherynne')
    persons.remove('Chuy')
    double_beds.remove(bed)

# assign persons to double beds
for i in range(2):
    bed = double_beds[i]
    if bed not in bed_assignments:
        bed_assignments[bed] = []
    for j in range(2):
        if persons:
            person = random.choice(persons)
            persons.remove(person)
            bed_assignments[bed].append(person)

# assign persons to single beds
for i in range(2):
    bed = single_beds[i]
    if bed not in bed_assignments:
        bed_assignments[bed] = []
    if persons:
        person = random.choice(persons)
        persons.remove(person)
        bed_assignments[bed].append(person)

# set up the email body
body=''

# print bed assignments
for bed, persons in bed_assignments.items():
    print(bed, ':', ', '.join(persons))
    body += f'{bed}={persons}\n'

# set up the email parameters
sender_email = 'fabianmendoza.py@gmail.com'
sender_password = os.environ.get("GMAIL_KEY")
receiver_email = os.environ.get("EMAILS")
subject = 'Sorteo de camas'

# create the email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# connect to the SMTP server and send the email
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email, receiver_email, message.as_string())
    print('Email sent successfully')