# this program sends emails from my gmail account
# to any specified email

import smtplib, ssl
import pandas as pd
import datetime as dt
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
    send_email()
    
def send_email():
    port = 465  # For SSL
    sender_email = "alfredmathew718@gmail.com"
    receiver_email = "alfredmathew@outlook.com"  # Enter receiver address
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = 'Multipart Test'
    message['From'] = sender_email  # Enter your address
    message['To'] = receiver_email

    # use getpass module here
    password = input("Type your password and press enter: ")

    # Create the plain-text and HTML version of your message
    # text = '''\
    # Hi,
    # How are you?
    # Real Python has many great tutorials:
    # www.realpython.com'''
    html_file = open('./html/1.html','rt')
    html='''\
    '''
    for line in html_file:
        html+=f'{line}\n'
    html_file.close()
    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    with open('./img/1.jpg','rb') as attachment:
        part = MIMEBase('application','octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    message.attach(part)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def check_dates(given_date):
    now = dt.datetime.now()
    if now.month == given_date.month and now.day == given_date.day:
        return True
    else:
        return False

def open_data():
    data = pd.read_excel('./sample_data.xlsx')
    return data

def filter_data(data):
    list = []
    i = 0
    while i < data['Baptism-Date'].count():
        if check_dates(data['Baptism-Date'][i]):
            list.append(True)
        else:
            list.append(False)
        i += 1
    print(list)
    return pd.Series(list)

if __name__ == "__main__": main()