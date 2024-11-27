from fastapi import FastAPI, Request
from pydantic import BaseModel
from twilio.rest import Client
import uuid
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


app = FastAPI()

# Twilio configuration (Replace these with your actual Twilio credentials)
TWILIO_ACCOUNT_SID = 'ACffd1af5b6b76cb4105985c6a8e8a66f4'
TWILIO_AUTH_TOKEN = '61dc715c2053aeed58369ad1177743fb'
TWILIO_PHONE_NUMBER = '+18324971833'

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_email_via_sendgrid(to_email, subject, message):
    sg = sendgrid.SendGridAPIClient(api_key="your_sendgrid_api_key")
    from_email = Email("your_email@example.com")
    to_email = To(to_email)
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.send(mail)
        print(f"Message sent with status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

# Create Pydantic models
class PhoneRequest(BaseModel):
    phone_number: str

class LinkClickRequest(BaseModel):
    unique_id: str


@app.post("/send-link")
async def send_link():
    unique_id = str(uuid.uuid4())  # Generate unique ID for the link
    link = f"http://your-domain.com/click/{unique_id}"  # Link that user will click
    # Send the SMS with the link using Twilio
    to_email = "trivenisabale33@gmail.com"
    subject = "Test Message"
    message = "Hello, this is a mail for your future sefty." + link
    print("Message", message)
    send_email_via_sendgrid(to_email, subject, message)
    return {"message": "Link sent successfully"}


@app.get("/click/{unique_id}")
async def link_click(unique_id: str, request: Request):
    # Get the IP address of the requestor
    ip_address = request.client.host
    # Store or log the IP address as required (can save in DB or log file)
    return {"message": "Link clicked!", "ip_address": ip_address, "unique_id": unique_id}


