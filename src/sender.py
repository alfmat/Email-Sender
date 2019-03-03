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
# this was initially imported for image editing
#from PIL import Image, ImageDraw, ImageFont
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
    data = open_data()
    data = data[filter_data(data)]
    process_person(data)

def send_email(**kwargs):
    """send_email(**kwargs) --> this is the function that sends out emails

    Key word arguments:
    child -- requires a string that contains the child's name (no default)
    dad -- requires a list with dad's name and email address
    mom -- requires a list with mom's name and email address
    gmom -- requires a list with grandmother's name and email address
    gdad -- requires a list with grandfather's name and email address

    Outcomes:
    * Emails are sent to all people who's baptism date matches the current
    date.
    """
    port = 465  # For SSL
    sender_email = "alfredmathew718@gmail.com"
    # receiver_email = "alfredmathew718@gmail.com"
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = 'Baptism Anniversary - STM Charismatic Group'
    message['From'] = sender_email  # Enter your address
    # use getpass module here or keyring module
    password = kr.get_password('gmail','alfredmathew718')
    imgno = 5 #randint(1,4)
    # edit_image(imgno,first_name,last_name)
    with open(f'../img/resources/{imgno}.png','rb') as attachment:
        part = MIMEBase('application','octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    # part.add_header(
    #     "Content-Disposition",
    #     "attachment; filename = BaptismAnniversary.jpg",
    # )
    part.add_header(
        'Content-ID',
        '<image1>'
    )
    message.attach(part)

    for k in kwargs:
        if k == 'child':
            continue
        else:
            html='''\
            <html>
            <head>
                <title>Charismatic Group Wishes</title>
                <style>
                        header {
                            width: 100%;
                            height: 20%;
                        }
                        p {
                            font-family: 'Times New Roman', Times, serif;
                            font-size: 14pt;
                        }
                        #chpic {
                            height: 450pt;
                            width: 500pt;
                        }
                        h1 {
                            font-size: 20pt ;
                        }
                        footer {
                            width: 100%;
                        }
                </style>
            </head>\n'''
            html += f'''
            <body>
                <header>
                    <h1>
                        Greetings from the STM Charismatic Prayer Group!
                    </h1>
                </header>
                <article>
                    <p>
                        <header>
                        <h2>
                        Dear {kwargs[k][0]},
                        </h2>
                        </header>
                    </p>
                    <p>
                        <header>
                        <h3>
                        We would like to wish your child {kwargs['child']} a happy baptism anniversary!
                        </h3>
                        </header>
                    </p>
                    <img id="chpic" src="cid:image1">
                    <p>
                    <br>
                    <br>
                    <br>
                    <h2>
                    ABOUT Life in Christ Charismatic Prayer Group </h2>
                    ............................................................................<br>
                    <h3>
                        We strive to deepen the prayer lives of participants and their dependence<br>
                        on the Holy Spirit in all aspects of their daily life. We hope to broaden<br>
                        participants' knowledge of and openness to the gifts, fruits, charisms, <br>
                        and manifestations of the Holy Spirit.
                    </h3>
                    </p>
                    <p>
                        We meet on the 2nd and 4th Tuesdays of every month.
                    </p>
                </article>
                <footer>
                    <section>
                        <address>
                            <p>
                                Contact Matt Sebastian:
                                <ul>
                                    <li>+1.919.519.2490</li>
                                    <li>sebastianmatt@gmail.com</li>
                                </ul>
                            </p>
                        </address>
                    </section>
                    <section>
                        <address>
                            <p>
                                <a href="https://stmchapelhill.org/charismatic-prayer-group">Here is some more info about us!</a>
                            </p>
                        </address>
                    </section>
                </footer>
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
            receiver_email = kwargs[k][1]

            # checks if the receiver_email is null
            if(receiver_email == np.nan):
                continue

            # attaches html to the file
            message.attach(part2)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                message['To'] = receiver_email
                server.sendmail(sender_email, receiver_email, message.as_string())
                server.quit()
            print('Message Sent to family of {}!'.format(kwargs['child']),flush=True)
            break

def process_person(data):
    """process_person(data) --> takes each person in the data set and sends emails to relatives

    Parameters:
    data -- this is a pandas DataFrame that contains information about
    the people whose baptism dates match the current date

    Outcomes:
    * send_email method is called until each person in the DataFrame has been sent
    emails
    """
    length = len(data.index)
    i=0
    while i < length:
        person = data.iloc[i]
        send_email(
            child = ' '.join([person['Baptized-Firstname'],person['Batpized-Lastname']]),
            dad = [' '.join([person['Father-Firstname'],person['Father-Lastname']]),person['Father-Email']],
            mom = [' '.join([person['Mother-Firstname'],person['Mother-Lastname']]),person['Mother-Email']],
            gmom = [' '.join([person['Godmother-Firstname'],person['Godmother-Lastname']]),person['Godmother-Email']],
            gdad = [' '.join([person['Godfather-Firstname'],person['Godfather-Lastname']]),person['Godfather-Email']]
        )
        i+=1

def check_dates(given_date):
    """check_dates(given_date) --> checks if the given datetime object has the same
    day and month as the current date

    Parameters:
    given_date -- this is a datetime object that contains at least a month and a day

    Outcomes:
    * Function returns True if the datetime object given to it matches the current
    month and day
    """
    now = dt.datetime.now()
    if now.month == given_date.month and now.day == given_date.day:
        return True
    else:
        return False

def open_data():
    data = pd.read_excel('../data/sample_data.xlsx')
    # cleans the data
    data.dropna(thresh=13)
    return data

def filter_data(data):
    """filter_data(data)

    Parameters:
    data -- pandas DataFrame that contains information about parishioners including their godparents,
    and parents

    Outcomes:
    * goes through the DataFrame and uses check_dates method to see if the datatime object
    of the current row matches the current date
    * returns a pandas Series that contains boolean values and is used to filter the
    DataFrame for children with current baptism days
    """
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

# def edit_image(imgno,first_name,last_name):
#     img = Image.open(f'../img/resources/{imgno}.png')
#     draw = ImageDraw.Draw(img)
#     # font = ImageFont.truetype(<font-file>, <font-size>)
#     font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 30)
#     # draw.text((x, y),"Sample Text",(r,g,b))
#     draw.text((200, 50),f"{first_name} {last_name}",(39,40,48),font=font)
#     img.save('../img/new/sample-out.png')

if __name__ == "__main__": main()
