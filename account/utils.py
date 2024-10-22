import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length=6):
    # generate a random otp code
    otp = ''.join(random.choices(string.digits, k=length))
    return otp

def send_otp_email(to_email, otp):
    subject = "Your OTP code"
    message = "Your OTP code is: {}".format(otp)
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])