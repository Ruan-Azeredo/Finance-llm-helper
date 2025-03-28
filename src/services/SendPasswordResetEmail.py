from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import os

def _load_env_environment():

    load_dotenv()

    FRONTEND_URL = os.getenv("FRONTEND_URL")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    if not all([FRONTEND_URL, EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS]):
        raise ValueError("Uma ou mais variáveis de ambiente não foram carregadas corretamente!")

    return FRONTEND_URL, EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS


def SendPasswordResetEmail(user_email: str, reset_token: str):

    FRONTEND_URL, EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS = _load_env_environment()

    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    msg = EmailMessage()
    msg["Subject"] = "Redefinição de senha"
    msg["From"] = EMAIL_USER
    msg["To"] = user_email
    msg.set_content(f"Clique no link abaixo para redefinir sua senha:\n{reset_link}")
    msg.add_alternative(
        f"""
        <p>Clique no link abaixo para redefinir sua senha:</p>
        <a href="{reset_link}">Redefinir senha</a>
        <p>Se você não solicitou a redefinição de senha, ignore este email.</p>
        """,
        subtype="html"
    )

    print(EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS)
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS +  's')
        server.send_message(msg)
        print("Email sent successfully")
    except Exception as error:
        print(f"Error sending email: {error}")
        Exception(f"Error sending email: {error}")