import random
import smtplib
from email.message import EmailMessage

EMAIL_SENDER = "mf0583275242@gmail.com"
EMAIL_PASSWORD = "gjzrznpbzvzfsmzw"
EMAIL_RECEIVER = "m0544195828@email.com"

def generate_random_image_urls(n=10):
    return [f"https://picsum.photos/seed/{random.randint(1000,9999)}/800/500" for _ in range(n)]

def send_email(image_urls):
    msg = EmailMessage()
    msg["Subject"] = "📸 10 תמונות אקראיות מ־picsum"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    body = "הנה 10 תמונות אקראיות (ללא API):\n\n" + "\n".join(image_urls)
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    urls = generate_random_image_urls()
    send_email(urls)
