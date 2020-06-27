import os
import requests
import urllib.request
import time

import smtplib

from bs4 import BeautifulSoup
from datetime import datetime
from email.message import EmailMessage

from recipients import recipients
from config import pw, url, sender

# Initialize log location
log_path = 'logs/'
sent_mails_log = log_path + 'sent_mails.csv'

# Get HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# Get current week no. & week no. on website
h1 = soup.find('h1')
header_week_no = h1.text.split(' ')[-1]
header_week_no = int(header_week_no)

current_week_no = datetime.today().isocalendar()[1]

# Check if mail has already been sent successfully
not_yet_sent = True

if os.path.isfile(sent_mails_log):
    with open(sent_mails_log, 'r') as f:
        for last_line in f:
            pass

    last_mail_ts = last_line.split(',')[0]
    last_mail_ts = datetime.strptime(last_mail_ts, '%Y-%m-%d %H:%M:%S').date()

    if last_mail_ts >= datetime.today().date():
        not_yet_sent = False



if header_week_no != current_week_no:
    if not_yet_sent:
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{now} - NEW WORKOUTS ONLINE NOW')


        ### parse relevant content from the html
        def replace_with_newlines(element):
            '''reads html into a string and replaces <br> with newlines'''
            text = ''
            for elem in element.recursiveChildGenerator():
                if isinstance(elem, str):
                    text += elem.strip()
                elif elem.name == 'br':
                    text += '\n'
                elif elem.name == 'strong':
                    text += '\n'
            return text


        days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"]
        workouts = {}

        try:
            for day in days:
                day_divs = soup.find("div", {"id": day})

                content = day_divs.find("div", {'class': 'elementor-text-editor elementor-clearfix'})
                full_day = replace_with_newlines(content)
                full_day = full_day.strip()
                
                wod = ''
                endurance = ''
                last_header = ''

                for line in full_day.split('\n'):
                    line = line.strip()

                    if line.upper() == 'WOD' or line.upper() == 'ENDURANCE' or line.upper() == 'BASIC':
                        last_header = line.upper()

                    else:
                        if last_header == 'WOD' and len(line)>0:
                            wod += line + '\n'
                        elif last_header == 'ENDURANCE' and len(line)>0:
                            endurance += line + '\n'
                            
                workouts[day.capitalize()] = {
                    'WOD': wod,
                    'ENDURANCE': endurance
                }


            ### extract workout infos into string
            mail_content = ""

            for day, exercises in workouts.items():
                mail_content += day
                mail_content += '\n\n'
                
                for type_, content in exercises.items():
                    if len(content) > 0:
                        mail_content += (type_ + '\n')
                        mail_content += (content + '\n')
                    
                mail_content += '\n'

            now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{now} - CONTENT PARSED SUCCESSFULLY')


        except Exception as ex:
            now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{now} - ERROR PARSING CONTENT - {type(ex)} {ex}')


        ### send mail
        try:
            msg = EmailMessage()
            msg.set_content(mail_content)

            msg['Subject'] = f'Workouts KW{header_week_no} jetzt online!'
            msg['From'] = sender
            msg['To'] = recipients

            s = smtplib.SMTP('smtp.gmail.com', 587) 
            s.starttls() 
            s.login(msg['From'], pw) 

            s.send_message(msg)
            s.quit()


            now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            # create `logs` dir if it does not exist
            if not os.path.isdir('logs'):
                os.mkdir('logs')
                # create logs.csv with headers
                with open(sent_mails_log, 'w+') as f:
                    f.write('date,recipients\n')

            # append current date 
            with open(sent_mails_log, 'a') as f:
                rec_str = '|'.join(recipients)
                f.write(f'{now},{rec_str}\n')
            
            print(f'{now} - MAIL SENT SUCCESSFULLY')
                

        except Exception as ex:
            now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{now} - ERROR SENDING MAIL - {type(ex)} - {ex}')

    else:
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{now} - ATTEMPT - E-MAIL ALREADY SENT')

else:
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{now} - ATTEMPT - WORKOUTS NOT YET ONLINE')
