# this program sends emails from my gmail account
# to any specified email

import smtplib, ssl
import pandas as pd
import getpass as gp
import numpy as np
import socket
import keyring as kr
import datetime as dt
from random import randint
from PIL import Image, ImageDraw, ImageFont
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    
def main(): 
    send_email('Alfred','Mathew')

def send_email(first_name, last_name):
    port = 465  # For SSL
    sender_email = "alfredmathew718@gmail.com"
    receiver_email = "alfredmathew@outlook.com"  # Enter receiver address
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = 'Baptism Anniversary - STM Charismatic Group'
    message['From'] = sender_email  # Enter your address
    message['To'] = receiver_email

    # use getpass module here
    password = kr.get_password('gmail','alfredmathew718')

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

    edit_image(1,first_name,last_name)

    with open('./img/new/sample-out.jpg','rb') as attachment:
        part = MIMEBase('application','octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment; filename = BaptismAnniversary.jpg",
    )

    message.attach(part)
  
    # with smtplib.SMTP(socket.gethostname(), port=465) as server:
    #      server.sendmail(sender_email, receiver_email, message.as_string())
    # smtpObj = smtplib.SMTP(host='192.168.86.95',port=465)
    # smtpObj.sendmail(sender_email, receiver_email, message.as_string())         
    # print("Successfully sent email")
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    print('Message Successfully Sent!')

def process_person(data):
    length = len(data.index)
    i=0
    first_name = ''
    last_name = ''
    while i < length:
        first_name = data.iloc[i]['Baptized-Firstname']
        last_name = data.iloc[i]['Batpized-Lastname']
        send_email(first_name,last_name)
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
    img = Image.open(f'./img/{imgno}.jpg')
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 30)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((200, 50),f"{first_name} {last_name}",(39,40,48),font=font)
    img.save('./img/new/sample-out.jpg')

if __name__ == "__main__": main()