from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from src.utils.settings import settings


# Email request schema
class EmailSchema(BaseModel):
    email: List[EmailStr]


# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Hardik",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


# Function to send emails
async def send_emails(emails: List[EmailStr]):
    html = """
    <p>Hi, this is a test mail. Thanks for using FastAPI-Mail!</p>
    """

    message = MessageSchema(
        subject="FastAPI-Mail module",
        recipients=emails,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"message": "Email has been sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"message": f"Email sending failed: {e}"}
