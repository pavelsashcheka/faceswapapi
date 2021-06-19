import base64
from email.mime.image import MIMEImage
from io import BytesIO

from PIL import Image
from django.core.mail import EmailMultiAlternatives

from rest import settings


def send_image_via_email(request, result_image, result_string):
    if 'email' in request.data:
        recipient = request.data['email']
        sender = settings.EMAIL_HOST_USER
        result_name = str(result_image.name)

        pillow_image = Image.open(BytesIO(base64.b64decode(result_string)))
        path = f"/home/braindeadpaul/braindeadpaul.pythonanywhere.com/uploaded_pictures/pictures/results/{result_name}"

        pillow_image.save(path)

        subject = 'Фотография'

        body_html = '''
        <html>
            <body>
                <img src="cid:logo.png" />
            </body>
        </html>
        '''
        message = EmailMultiAlternatives(
            subject,
            body_html,
            from_email=sender,
            to=[recipient]
        )
        message.mixed_subtype = 'related'
        message.attach_alternative(body_html, "text/html")

        with open(path, 'rb') as file:
            email_image = MIMEImage(file.read())
            email_image.add_header('Content-ID', '<{name}>'.format(name=result_name))
            email_image.add_header('Content-Disposition', 'inline', filename=result_name)
        message.attach(email_image)
        message.send()