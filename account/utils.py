from django.core.mail import send_mail
from decouple import config



def send_activation_code(email, activation_code):
    activation_url = f'http://127.0.0.1:8000/api/v1/account/activate/{activation_code}'
    message =''''''
    html = f"""
    <h1>перейдите по ссылке</h1>
    <a href="{config('LINK')}api/v1/account/activate/{activation_code}">
    <button>Activate</button>
    </a>

    """
    send_mail(
        subject = 'Activate your account',
        message=message,
        from_email='test@test.com',
        recipient_list=[email,],
        html_message=html,
    )
