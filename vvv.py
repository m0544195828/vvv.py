import requests
import smtplib
from email.message import EmailMessage
import os

def download_images(count=10):
    image_data_list = []
    for i in range(count):
        url = f"https://picsum.photos/600/400?random={i}"
        response = requests.get(url)
        if response.status_code == 200:
            image_data_list.append({
                "filename": f"image_{i+1}.jpg",
                "data": response.content
            })
    return image_data_list

def send_email_with_images(sender_email, sender_password, recipient_email, subject, body, images):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(body)

    for img in images:
        msg.add_attachment(img["data"],
                           maintype="image",
                           subtype="jpeg",
                           filename=img["filename"])

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

if __name__ == "__main__":
    YOUR_EMAIL = os.environ["SENDER_EMAIL"]
    YOUR_PASSWORD = os.environ["SENDER_PASSWORD"]
    RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

    try:
        images = download_images()
        send_email_with_images(
            YOUR_EMAIL,
            YOUR_PASSWORD,
            RECEIVER_EMAIL,
            "📷 תמונות אקראיות מ-Picsum",
            "מצורפות 10 תמונות",
            images
        )
        print("✅ ההודעה נשלחה בהצלחה!")
    except Exception as e:
        print("❌ אירעה שגיאה:", e)

