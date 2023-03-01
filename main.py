import os
import random
import smtplib
import json
from email.mime.text import MIMEText

double_beds = ['Double Bed bedroom 1', 'Double Bed bedroom 2', 'Double Bed living room']
single_beds = ['Single Bed 1', 'Single Bed 2']
persons_json = os.environ.get("PERSONS_LIST")
persons = json.loads(persons_json)
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

# connect to the SMTP server and send the email
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

# set up the email parameters
sender = 'fabianmendoza.py@gmail.com'
password = os.environ.get("GMAIL_KEY")
receiver_email_json = os.environ.get("EMAILS")
recipients = json.loads(receiver_email_json)
subject = 'Sorteo de camas'

send_email(subject, body, sender, recipients, password)