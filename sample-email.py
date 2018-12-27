from smtplib import SMTP
SERVER = "localhost"

FROM = 'monty@python.com'

TO = ["alfredmathew718@gmail.com"] # must be a list

SUBJECT = "Hello!"

TEXT = "This message was sent with Python's smtplib."

# Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail
with SMTP() as server:
    server.connect(host='localhost')
    server.sendmail(FROM, TO, message)
    server.quit()