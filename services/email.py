from fastapi import BackgroundTasks
import os 
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("EMAIL")
sender_email_password = os.getenv("PASSWORD")

def send_email(to_email: str, subject: str, content: str):
    """
    Send an email using SMTP.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        content (str): The HTML content of the email body.
        sender_email (str): The sender's email address.
        sender_email_password (str): The sender's email password for authentication.

    Raises:
        Exception: If sending the email fails.
    """
    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(content, 'html'))

    try:
        # Set up the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_email_password)  # Log in to the server
            server.sendmail(sender_email, to_email, msg.as_string())  # Send the email
            logging.info(f"Email sent successfully to {to_email}")

    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}")
        raise

def send_invite_email(to_email: str):
    '''Send an invitation email to a user.'''

    subject = "You're invited to join the platform!"
    content = "<h1>Welcome!</h1><p>You're invited to join our platform.</p>"
    send_email(to_email, subject, content)

def send_password_update_email(to_email: str):
    '''Send a password update notification email to the user'''
    
    subject = "Password Update Notification"
    content = """
    <html>
    <body>
        <p>Hello,</p>
        <p>Your password has been successfully updated. If you did not initiate this change, please contact support immediately.</p>
    </body>
    </html>
    """
    
    send_email(to_email=to_email, subject=subject, content=content)