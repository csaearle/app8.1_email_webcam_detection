import ssl, smtplib
from PIL import Image
from io import BytesIO
from email.message import EmailMessage
import os

SENDER = "csaearle69@gmail.com"
PASSWORD = os.getenv("SAFE_PASSWORD")
RECEIVER = "csaearle69@gmail.com"
def send_email(image_path):

    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hi, A new customer just walked in!")

    with open (image_path, "rb") as file:
        content = file.read()

    image_data = BytesIO(content)
    image = Image.open(image_data)
    image_format = image.format

    email_message.add_attachment(content, maintype="image", subtype=image_format)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/19image.png")
    






"""
    username = "csaearle69@gmail.com"
    password = os.getenv("SAFE_PASSWORD")
    receiver = "csaearle69@gmail.com"

    host = "smtp.gmail.com"
    port = 456
    context = ssl.create_default_context()


    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

"""