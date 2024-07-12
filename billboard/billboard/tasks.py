from celery import shared_task
import datetime
import time
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from advertisement.models import Advertisement, Author

@shared_task
def weekly_task():

    authors = Author.objects.all()
    
    html_content = render_to_string(
        'news_sending.html',
    )

    msg = EmailMultiAlternatives(
        subject='Weekly',
        body='',
        from_email=None,
        to=authors,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()