import email, smtplib, ssl, pickle

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from getpass import getpass


class SendMail:
    def __init__(self):
        try:  # load credentials from file
            with open("credentials.pickle", "rb") as f:
                self.password = pickle.load(f)
        except FileNotFoundError:
            self.password = getpass("Password: ")
            if input("Save password? [y/n]: ").lower() == "y":
                with open("credentials.pickle", "wb") as f:
                    pickle.dump(self.password, f)
        self.sender_email = "odpadzreklam@seznam.cz"
        self.receiver_email = "frantisek.clupny@email.cz"
        self.smtp_server = "smtp.seznam.cz"
        self.port = 465  # For starttls

    def send_mail(self, file: str):

        filename = file.split("/")[-1]  # exract filename from path

        self.subject = f"Teploty z {filename}"
        self.body = "Data jsou v příloze"

        # Create a multipart self.message and set headers
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = self.subject
        self.message["Bcc"] = self.receiver_email  # Recommended for mass emails

        # Add body to email
        self.message.attach(MIMEText(self.body, "plain"))

        # Open PDF file in binary mode
        with open(file, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header("Content-Disposition", "attachment", filename=f"{filename}.csv")

        # Add attachment to self.message and convert self.message to string
        self.message.attach(part)
        text = self.message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)
