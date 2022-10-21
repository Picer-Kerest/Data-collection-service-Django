import asyncio
import codecs
import os
import sys
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from scraping.parsers import *




PROJECT_NAME = 'scraping_service'


def main():
    from scraping.models import Vacancy, City, Language, Error, Url

    proj = os.path.dirname(os.path.abspath('manage.py'))
    sys.path.append(proj)


    User = get_user_model()  # Link to the current user model

    parsers = (
        (habr, 'habr'),
        (hh, 'hh')
    )

    jobs, errors = [], []

    def get_settings():
        qs = User.objects.filter(send_email=True).values()  # values() for Dictionary Lists
        # <QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
        settings_lst = set((q['city_id'], q['language_id']) for q in qs)
        return settings_lst

    def get_urls(_settings):
        '''
        Мы получаем пару из города и языка, которые у нас есть на сайте среди пользователей.
        Далее мы забираем из базы все значения {(город, язык): urls}
        Проходим по каждой паре среди пользователей и проверяем есть ли она в базе на соответствие {(город, язык): urls}
        Дальше в словарь помещаем ключ города и его id, то же самое с языком и потом если есть url для этой пары,
        то добавляем url.
        В конце добавляем этот словарь в массив urls.
        '''
        qs = Url.objects.all().values()
        url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
        urls = []
        for pair in _settings:
            if pair in url_dict:
                tmp = {}
                tmp['city'] = pair[0]
                tmp['language'] = pair[1]
                url_data = url_dict.get(pair)
                if url_data:
                    tmp['url_data'] = url_dict.get(pair)
                    urls.append(tmp)
        return urls


    async def search_func(value):
        func, url, city, language = value
        job, err = await loop.run_in_executor(None, func, url, city, language)
        errors.extend(err)
        jobs.extend(job)


    settings = get_settings()
    url_lst = get_urls(settings)


    # asyncio
    loop = asyncio.new_event_loop()    # https://aiopg.readthedocs.io/en/stable/run_loop.html
    tmp_tasks = [(func, data_url['url_data'][key], data_url['city'], data_url['language'])
                 for data_url in url_lst
                 for func, key in parsers]
    '''
    Tuple со всеми url'ами, городами, языками, которые у нас есть
    '''

    # tasks = asyncio.wait([loop.create_task(search_func(task)) for task in tmp_tasks])
    '''
    search_func для добавления работы/ошибок
    task - набор данных func, data_url['url_data'][key], data_url['city'], data_url['language']
    loop.create_task создаёт таски 
    asyncio.wait вызывает на выполнение 
    '''

    # for data_url in url_lst:
    #     for func, key in parsers:
    #         url = data_url['url_data'][key]
    #         j, e = func(url, city=data_url['city'], language=data_url['language'])
    #         jobs += j
    #         errors += e

    if tmp_tasks:
        tasks = asyncio.wait([loop.create_task(search_func(task)) for task in tmp_tasks])
        loop.run_until_complete(tasks)
        loop.close()

    for job in jobs:
        v = Vacancy(**job)
        try:
            v.save()
        except DatabaseError:
            pass

    if errors:
        er = Error(data=errors).save()  # JSONdata [{}, {}, {}, {}, ...{}]

    # h = codecs.open('work.txt', 'w', 'utf-8')
    # h.write(str(jobs))
    # h.close()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
    import django

    django.setup()
    main()