#   https://realpython.com/python-send-email/

import smtplib, ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

stub_sender_email = "systemintegration2023@gmail.com"
stub_password = "mwyctkhksjvlockr"


def send_email(receiver_email, random_auth_code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verification Code"
    message["From"] = stub_sender_email
    message["To"] = receiver_email

    content = f"Hi, your verification code is: {random_auth_code}"
    print(content)

    # Create the plain-text and HTML version of your message
    text = f"""\
  {content}
  """

    html = f"""\
  <html>
    <body>
      <p>
        Hi,<br>
        <b>{content}</b><br>
      </p>
    </body>
  </html>
  """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(stub_sender_email, stub_password)
            server.sendmail(stub_sender_email, receiver_email, message.as_string())
        except Exception as ex:
            print(ex)
