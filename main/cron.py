from django.core.mail import send_mail
from django.template.loader import render_to_string

from main.models import Mails, Client, Logs
from django.utils import timezone

def send_periodic_email():
    try:
        mails = Mails.objects.filter(status=False)
        for mail in mails:
            response = 'Не поступил'
            if not mail.logs:
                logs = Logs.objects.create()
                mail.logs = logs

            current_time = timezone.now()
            try:
                if mail.scheduled is None or mail.scheduled <= current_time:
                    if mail.periodic is None:
                        response = send_mails(mail.theme, mail.body, mail.users.all().values_list('email', flat=True))
                        mail.status = True
                        mail.logs.status = True
                        mail.logs.last_time = current_time
                        mail.logs.response = response
                    elif not mail.end <= current_time:
                        mail.periodic -= 1
                        if mail.periodic == 0:
                            response = send_mails(mail.theme, mail.body, mail.users.all().values_list('email', flat=True))
                            mail.periodic = mail.dynamic_periodic
                            mail.logs.status = True
                            mail.logs.last_time = current_time
                            mail.logs.response = response
                    else:
                        mail.status = True
                        mail.logs.status = True
                        mail.logs.response = response
                mail.logs.save()
                mail.save()



            except Exception as error:
                print(f'Возникла ошибка:\n {error}')

                mail.logs.status = False
                mail.logs.last_time = timezone.now()
                mail.logs.response = response

                mail.logs.save()
                mail.save()
    except Exception as error:
        print(f'Возникла ошибка:\n {error}')

def send_mails(theme, body, recipient_emails):
    mail_subject = f'{theme}'
    message = render_to_string('main/send_email.html', {
        'theme': mail_subject,
        'body': body,
    })
    response = send_mail(mail_subject, message, 'sendinfoforauth@gmail.com', recipient_emails)
    print('email sent')
    return response