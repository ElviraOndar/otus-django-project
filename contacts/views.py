from django.shortcuts import render, redirect
from django.contrib import messages  # Для отображения сообщений пользователю
from .forms import ContactForm
from .tasks import send_contact_email_task  # Импортируем нашу Celery задачу


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Вызываем Celery задачу для асинхронной отправки писем
            send_contact_email_task.delay(name, email, subject, message)

            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact')  # Перенаправляем на ту же страницу
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact.html', {'form': form})


