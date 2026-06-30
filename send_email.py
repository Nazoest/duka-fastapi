""" import requests

"02af52f340bd745c3dd4b3cd8bd2d304"

ELASTIC_API_KEY="C4E230D42714698062B9B05C2651D4D5CDE6335B418F9D7170C9E8ECA7964CAF4F787A287903E1FC54EF7215651DF9DB"
FROM_EMAIL="nathanmacharia115@gmail.com"

url = "https://api.elasticemail.com/v2/email/send"


def send_email(to_email, subject, message):
    data={
        "apikey": ELASTIC_API_KEY,
        "from": FROM_EMAIL,
        "to": to_email,
        "subject": subject,
        "body": message
    }
    response = requests.post(url, data=data)
    return response.json()

print(send_email("nathanmacharia115@gmail.com", "test", "hello world")) """


import mailtrap as mt

def send_email(to_email, subject, message):
    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="DukaFastAPI"),
        to=[mt.Address(email=to_email)],
        subject=subject,
        text=message
    )
    client = mt.MailtrapClient(token="02af52f340bd745c3dd4b3cd8bd2d304")
    response = client.send(mail)
    
    return response

#print(send_email("nathanmacharia115@gmail.com", "payment", "hello nathan, this is a test email to confirm that your payment was successful. Thank you for using our service!"))

""" client = mt.MailtrapClient(token="02af52f340bd745c3dd4b3cd8bd2d304")
response = client.send(mail)

print(response) """