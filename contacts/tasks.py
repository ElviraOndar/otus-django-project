from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def send_contact_email_task(name, email, subject, message):
    """Отправляет письмо администратору и пользователю после отправки формы контактов"""
    admin_email = settings.DEFAULT_FROM_EMAIL  # email администратора
    site_name = "CodeCourse"
    # 1. Письмо администратору
    admin_context = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
    }
    admin_html_message = render_to_string('emails/admin_notification.html', admin_context)
    admin_email_subject = f'Новое сообщение с сайта {site_name}: {subject}'

    msg_to_admin = EmailMessage(
            admin_email_subject,
            admin_html_message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
        )
    msg_to_admin.content_subtype = "html" # Основной тип содержимого - HTML
    msg_to_admin.send(fail_silently=False) # fail_silently=False для отладки

    # 2. Письмо пользователю
    user_context = {
            'name': name,
            'subject': subject,
            'site_name': site_name,
        }
    user_html_message = render_to_string('emails/user_confirmation.html', user_context)
    user_email_subject = f'Ваше сообщение на сайте {site_name} принято'

    msg_to_user = EmailMessage(
            user_email_subject,
            user_html_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],  # Отправляем на email, указанный пользователем
        )
    msg_to_user.content_subtype = "html"  # Основной тип содержимого - HTML
    msg_to_user.send(fail_silently=False)


