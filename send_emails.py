import datetime
import os
import sys

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

PROJECT_NAME = 'scraping_service'


def main():
    proj = os.path.dirname(os.path.abspath('manage.py'))
    sys.path.append(proj)
    from scraping.models import Vacancy, City, Language, Error, Url
    from scraping_service.settings import EMAIL_HOST_USER

    def database_appeal(model):
        dct = {}
        qs_g = model.objects.all().values('id', 'name')
        for el in qs_g:
            dct.setdefault(el['id'])
            dct[el['id']] = (el['name'])
        return dct

    ADMIN_USER = EMAIL_HOST_USER
    today = datetime.date.today()
    subject = f'Mailing of vacancies for {today}'
    text_content = f'Mailing of vacancies for {today}'
    from_email = EMAIL_HOST_USER
    empty = '<h2>Today there is nothing according to your preferences</h2>'

    User = get_user_model()
    qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
    # Now only the specified keys will be in this dictionary
    users_dct = {}
    for i in qs:
        if i['city'] and i['language']:
            # Additional condition for exclusion None type
            users_dct.setdefault((i['city'], i['language']), [])
            users_dct[(i['city'], i['language'])].append(i['email'])
    if users_dct:
        params = {'city_id__in': [], 'language_id__in': []}
        # __in - все значения, которые принадлежат этой паре
        for pair in users_dct.keys():
            params['city_id__in'].append(pair[0])
            params['language_id__in'].append(pair[1])
        qs = Vacancy.objects.filter(**params, timestamp=today).values()
        vacancies = {}
        for i in qs:
            vacancies.setdefault((i['city_id'], i['language_id']), [])
            vacancies[(i['city_id'], i['language_id'])].append(i)
        for keys, emails in users_dct.items():
            rows = vacancies.get(keys, [])
            html = ''
            for row in rows:
                html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
                html += f'<p>{row["description"]}</p>'
                html += f'<p>{row["company"]}</p><hr>'
                # f-string -> Double brackets are not needed
            final_html = html if html else empty
            for email in emails:
                to = email
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(final_html, "text/html")
                msg.send()

    qs = Error.objects.filter(timestamp=today)
    subject = ''
    text_content = ''
    to = ADMIN_USER
    content = ''
    if qs.exists():
        error = qs.first()
        data_1 = error.data.get('errors', [])
        if data_1:
            content += '<hr>'
            content += '<h2 align="center">Errors</h2>'
            for dictionary in data_1:
                content += f'<h3><a href="{dictionary["url"]}">Error: {dictionary["title"]}</a></h3>'
            subject = f'Scraping Errors {today}'
            text_content = f'Scraping Errors {today}'
        data_2 = error.data.get('user_data', [])
        if data_2:
            content += '<hr>'
            content += '<h2 align="center">User wishes</h2>'
            for dictionary in data_2:
                content += f'<h3>You need to add settings for city {dictionary["city"]} and ' \
                           f'language {dictionary["language"]}. Sent from {dictionary["email"]} </h3>'
            subject = f'User wishes {today}'
            text_content = f'User wishes {today}'
    qs = Url.objects.all().values('city', 'language')
    urls_dct = {(i['city'], i['language']): True for i in qs}
    urls_err = ''
    cities_dct = database_appeal(City)
    language_dct = database_appeal(Language)
    for keys in users_dct.keys():
        if keys not in urls_dct:
            content += '<hr>'
            content += '<h2 align="center">Information about missing settings</h2>'
            if keys[0] and keys[1]:
                urls_err += f'<h3>For the city <b>{cities_dct[keys[0]]}</b> with <b>id={keys[0]}</b>, ' \
                            f'and language <b>{language_dct[keys[1]]}</b> ' \
                            f'with <b>id={keys[1]}</b> there are no scraping-urls</h3><br>'
    if urls_err:
        subject += 'Missing urls'
        content += urls_err

    if subject:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(content, "text/html")
        msg.send()

    # Another method of sending
    # import smtplib
    # from email.mime.multipart import MIMEMultipart
    # from email.mime.text import MIMEText
    #
    # msg = MIMEMultipart('alternative')
    # msg['Subject'] = 'List of vacancies for {}'.format(today)
    # msg['From'] = EMAIL_HOST_USER
    # mail = smtplib.SMTP()
    # mail.connect(EMAIL_HOST, 25)
    # mail.ehlo()
    # mail.starttls()
    # mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    #
    # html_m = "<h1>Hello world</h1>"
    # part = MIMEText(html_m, 'html')
    # msg.attach(part)
    # mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
    # mail.quit()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
    import django

    django.setup()
    main()

