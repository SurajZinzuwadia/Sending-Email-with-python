import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465
subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
smtp_server = "smtp.gmail.com"
sender_email = "sender@gmail.com"
receiver_email = "receiver@gmail.com"
password = input("Type your password and press enter:")

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email

print("Choose type of Email you wants send:")
print("0: For simple text")
print("1: For sending files")

def zero():
    text = """\
    Hi,
    How are you?
   This is plain text part
    """
    html = """\
    <html>
    <body>
     <p>Hi,<br>
     How are you?<br>
    This is HTML part
    </p>
    </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    print("Hello")
    return message

def one():
    message.attach(MIMEText(body, "plain"))
    filename = "document"

    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)


    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    # text = message.as_string()
    return message

def indirect(i):
    switcher={
            0:zero,
            1:one,
            }
    func=switcher.get(i,lambda :'Invalid')
    return func()

x = input()
text = indirect(int(x))

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context= context) as server:
    server.login(sender_email ,password)
    server.sendmail(sender_email, receiver_email, text.as_string())