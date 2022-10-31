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
        # qs = Vacancy.objects.filter(**params).values()[:10]
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

    qs_e = Error.objects.filter(timestamp=today)
    if qs_e.exists():
        error = qs.first()
        data = error.data
        content = ''
        for dictionary in data:
            content += f'<h5><a href="{dictionary["url"]}">Error: {dictionary["title"]}</a></h5>'
            subject = f'Scraping Errors {today}'
            text_content = f'Scraping Errors {today}'
            to = ADMIN_USER
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(content, "text/html")
            msg.send()

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
    import django

    django.setup()
    main()

