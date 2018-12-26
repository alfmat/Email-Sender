# this program sends emails from my gmail account
# to any specified email

import smtplib, ssl
import pandas as pd

def main():
    data = open_data()
    print(data.info())
    
def send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "alfredmathew718@gmail.com"  # Enter your address
    receiver_email = "alfredmathew@outlook.com"  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def open_data():
    data = pd.read_excel('sample_data.xlsx')
    return data

if __name__ == "__main__": main()