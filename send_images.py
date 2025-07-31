import random
import smtplib
import requests
from email.message import EmailMessage
from email.utils import make_msgid

EMAIL_SENDER = "mf0583275242@gmail.com"
EMAIL_PASSWORD = "gjzrznpbzvzfsmzw"
EMAIL_RECEIVER = "m0544195828@email.com"

def generate_random_images(n=10):
    urls = [f"https://picsum.photos/seed/{random.randint(1000,9999)}/800/500" for _ in range(n)]
    images = []
    for i, url in enumerate(urls):
        response = requests.get(url)
        if response.ok:
            cid = make_msgid(domain="picsum.photos")
            images.append({
                "cid": cid[1:-1],  # remove <>
                "data": response.content,
                "filename": f"image{i+1}.jpg"
            })
    return images

def send_email_with_images(images):
    msg = EmailMessage()
    msg["Subject"] = "📸 תמונות אקראיות בגוף המייל"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    html_content = "<h3>הנה 10 תמונות אקראיות:</h3>"
    for img in images:
        html_content += f'<img src="cid:{img["cid"]}" style="margin:10px"><br>'

    msg.set_content("לצפייה בתמונות יש להפעיל תצוגת HTML.")
    msg.add_alternative(html_content, subtype='html')

    for img in images:
        msg.get_payload()[1].add_related(
            img["data"],
            maintype='image',
            subtype='jpeg',
            cid=f"<{img['cid']}>",
            filename=img["filename"]
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    images = generate_random_images()
    send_email_with_images(images)
