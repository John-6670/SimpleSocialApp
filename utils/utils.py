import jwt
import os
from django.core.mail import EmailMessage
from dotenv import load_dotenv


load_dotenv()


class EmailHelper:
    @staticmethod
    def send_email(user):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
                           os.environ.get('SECRET_KEY'), algorithm='HS256')
        email_subject = 'Verify your email'
        email_body = (f'Hi {user.username},\n'
                      f'Use the link below to verify your email:\n'
                      f'http://localhost:8000/users/verify-email/?token={token}')
        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()
