#!/usr/bin/env python3
# this program sends emails from my gmail account
# to any specified email

import smtplib, ssl
import pandas as pd
import getpass as gp
import numpy as np
import keyring as kr
import datetime as dt
from random import randint
from PIL import Image, ImageDraw, ImageFont
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    
def main(): 
    data = open_data()
    process_person(data)

def send_email(**kwargs):
    port = 465  # For SSL
    sender_email = "lifeinchrist.stm@gmail.com"
    receiver_email = "alfredmathew@outlook.com"  # Enter receiver address
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = 'Baptism Anniversary - STM Charismatic Group'
    message['From'] = sender_email  # Enter your address
    message['To'] = receiver_email

    # use getpass module here or keyring module
    password = kr.get_password('gmail','lic.stm')

    # Create the plain-text and HTML version of your message
    # text = '''\
    # '''
    # html_file = open('./html/1.html','rt')
    first_name = kwargs['first_name']
    last_name = kwargs['last_name']
    html='''\
    <html>
    <head>
        <title>Introduction to HTML</title>
        <style>
                header {
                    width: 100%;
                    height: 20%;
                }
                h1 {
                    font-size: 20pt ;
                }
                body {
                    background-color: beige;
                }
        </style>
    </head>\n''' 
    html += f'''
    <body>
        <header>
            <h1>
                Greetings from the Charismatic prayer group!
            </h1>
        </header>
        <p>
            We would like to wish your child {first_name} {last_name} a happy baptism anniversary!
        </p>
        <p>
            We meet on the 2nd and 4th Thursdays of every month.
        </p>
    </body>
    </html>
    '''
    # for line in html_file:
    #     html+=f'{line}\n'
    # html_file.close()

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    imgno = randint(1,4)
    # edit_image(imgno,first_name,last_name)
    with open(f'./img/resources/{imgno}.jpg','rb') as attachment:
        part = MIMEBase('application','octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment; filename = BaptismAnniversary.jpg",
    )
    message.attach(part)
    
    for k in kwargs:
        if k == 'first_name' or k == 'last_name':
            continue
        else:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                # receiver_email = kwargs[k]
                server.sendmail(sender_email, receiver_email, message.as_string())
                server.quit()
    print(f'Message Sent to family of {first_name} {last_name}!')

def process_person(data):
    length = len(data.index)
    i=0
    first_name = ''
    last_name = ''
    while i < length:
        first_name = data.iloc[i]['Baptized-Firstname']
        last_name = data.iloc[i]['Batpized-Lastname']
        mom_email = data.iloc[i]['Mother-Email']
        dad_email = data.iloc[i]['Father-Email']
        gmom_email = data.iloc[i]['Godmother-Email']
        gdad_email = data.iloc[i]['Godfather-Email']
        send_email(
        first_name = first_name,
        last_name = last_name,
        mom_email = mom_email,
        dad_email = dad_email,
        gmom_email = gmom_email,
        gdad_email = gdad_email
        )
        i+=1

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
        if data['Baptism-Date'][i] == np.NaN:
            list.append(False)
        elif check_dates(data['Baptism-Date'][i]):
            list.append(True)
        else:
            list.append(False)
        i += 1
    return pd.Series(list)

def edit_image(imgno,first_name,last_name):
    img = Image.open(f'./img/resources/{imgno}.jpg')
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 30)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((200, 50),f"{first_name} {last_name}",(39,40,48),font=font)
    img.save('./img/new/sample-out.png')

if __name__ == "__main__": main()