import smtplib, ssl, pickle, excelmaker, os, json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from getpass import getpass


class SendMail:
    def __init__(self) -> None:
        """try:  # load credentials from file
            with open("credentials.pickle", "rb") as f:
                self.password: str = pickle.load(f)
        except FileNotFoundError:
            self.password = getpass("Password: ")
            if input("Save password? [y/n]: ").lower() == "y":
                with open("credentials.pickle", "wb") as f:
                    pickle.dump(self.password, f)
        self.sender_email: str = "odpadzreklam@seznam.cz"
        self.receiver_email: str = "frantisek.clupny@email.cz"
        self.smtp_server: str = "smtp.seznam.cz"
        self.port: int = 465  # For starttls"""

        try:  # nefunguje
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("config.json not found")

        try:
            self.password: str = config["password"]
            self.sender_email: str = config["sender_email"]
            self.receiver_email: str = config["receiver_email"]
            self.smtp_server: str = config["smtp_server"]
            self.port: int = config["port"]
        except KeyError:
            # print all config; debug part
            print(f"Sender email: {self.sender_email}")
            print(f"Receiver email: {self.receiver_email}")
            print(f"SMTP server: {self.smtp_server}")
            print(f"Port: {self.port}")
            print(f"Password: {self.password}")
            # print all config type
            print(f"Sender email type: {type(self.sender_email)}")
            print(f"Receiver email type: {type(self.receiver_email)}")
            print(f"SMTP server type: {type(self.smtp_server)}")
            print(f"Port type: {type(self.port)}")
            print(f"Password type: {type(self.password)}")
            raise KeyError("config.json is not valid. Check README.md for more info")

    def send_mail(self, file: str) -> bool:

        if file.endswith((".csv", ".xlsx")):
            return True

        maxTemp, maxTempCas, minTemp, minTempCas, avg = excelmaker.make_excel(
            file
        )  # make excel file from csv
        # file += ".xlsx"  # add extension
        filename: str = file.split("/")[-1]  # exract filename from path

        self.subject: str = f"""Teploty z {". ".join(filename.split("-")[::-1])}"""
        self.body: str = f"Průměrná teplota byla {avg} °C\nNejvyšší teplota {maxTemp} °C v {maxTempCas}\nNejnižší teplota {minTemp} °C v {minTempCas}\nData jsou v příloze"

        file += ".xlsx"  # add extension
        filename: str = file.split("/")[-1]  # exract filename from path

        # Create a multipart self.message and set headers
        self.message: MIMEMultipart = MIMEMultipart()
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
            part: MIMEBase = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header("Content-Disposition", "attachment", filename=f"{filename}")

        # Add attachment to self.message and convert self.message to string
        self.message.attach(part)
        text: str = self.message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(
                self.smtp_server, self.port, context=context
            ) as server:
                server.login(self.sender_email, self.password)
                # for receiver in self.receiver_email: brakes for some reason
                server.sendmail(self.sender_email, self.receiver_email, text)
                os.replace(file, f"LOGGED/{filename}")  # move excel file
                return True
        except:
            return False


if __name__ == "__main__":
    try:
        for file in os.listdir("WIP"):
            if not file.endswith(".xlsx"):
                if SendMail().send_mail(f"WIP/{file}"):
                    print(f"Email sent for {file}")
    except FileNotFoundError:
        print("WIP folder not found")
