# coding: utf-8
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

# stolen from p36


def send_email(subject, from_email, recipient_list, message, html=False):
    """
    Wrapper to Django EmailMessage stuff
    """
    email = EmailMessage(subject, message,
                         from_email, recipient_list)
    if html:
        email.content_subtype = "html"
    email.send()
    return True


def send_email_template(subject, from_email, recipient_list,
                        template, context=None):
    """
    Simple wrapper to method `send_email` with
    template stuff.
    """
    # autoescape = True ?
    message = get_template(template).render(Context(context or {}))
    return send_email(
        subject=subject,
        from_email=from_email,
        recipient_list=recipient_list,
        message=message,
        html=True
    )
