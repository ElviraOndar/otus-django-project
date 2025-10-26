from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Отправка письма на почту админа
            send_mail(
                form.cleaned_data['subject'],
                f"От: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n{form.cleaned_data['message']}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            # Сообщение пользователю
            messages.success(request, "Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.")
            return redirect('contact')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ContactForm()
    return render(request, 'contacts/contact.html', {'form': form})


