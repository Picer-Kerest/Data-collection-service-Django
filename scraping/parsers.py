import requests
import codecs
from bs4 import BeautifulSoup as BS


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
     }
    # {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}



def rabota(url):
    #   RABOTA.RU
    jobs = []
    errors = []
    domain = 'https://spb.rabota.ru'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs={'class': 'vacancy-search-page__title-hint'})
        if not new_jobs:
            main_div = soup.find('div', attrs={'class': 'infinity-scroll r-serp__infinity-list'})
            if main_div:
                article_lst = main_div.find_all('article', attrs={'itemscope': 'itemscope'})
                for article in article_lst:
                    title = article.find('h3', attrs={'class': 'vacancy-preview-card__title'})
                    href = title.a['href']
                    tag_for_description = article.find('div', attrs={'class': 'vacancy-preview-card__short-description'})
                    content = tag_for_description.text
                    company = 'No name'
                    span = article.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                    if span:
                        company = span.text
                    jobs.append({
                        'url': domain + href,
                        'title': title.text,
                        'company': company,
                        'description': content,
                        # 'city': 1,
                        # 'language': 1,
                        # 'timestamp': 1,
                    })
            else:
                errors.append({
                    'url': url,
                    'title': 'Div does not exists',
                })
        else:
            errors.append({
                'url': url,
                'title': 'Page is empty',
            })
    else:
        errors.append({
            'url': url,
            'title': 'Page do not response',
        })

    return jobs, errors



def habr(url):
    # habr.ru
    jobs = []
    errors = []
    domain = 'https://career.habr.com'
    url = 'https://career.habr.com/vacancies?q=python&type=all'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', attrs={'class': 'section-group section-group--gap-medium'})
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'vacancy-card__inner'})
            for div in div_lst:
                title = div.find('div', attrs={'class': 'vacancy-card__company-title'})  # We turn to <h2>, then to <a>, then to href
                div_for_href = div.find('div', attrs={'class': 'vacancy-card__title'})
                href = div_for_href.a['href']  # Dot notation
                main_span_div = div.find('div', attrs={'class': 'vacancy-card__skills'})
                span_lst = main_span_div.find_all('span', attrs={'class': 'preserve-line'})
                content = ''
                if main_span_div and span_lst:
                    description_lst = []
                    for span in span_lst:
                        description_lst.append(span.a.text)
                        if len(description_lst) == 1:
                            description_lst.append(', ')
                    # after the end of the cycle, the description_lst will be filled
                    for el in description_lst:
                        content += el
                company = 'No name'
                logo = soup.find('div', attrs={'class': 'vacancy-card__company-title'})
                if logo:
                    company = logo.text
                jobs.append({
                    'url': domain + href,
                    'title': title.text,
                    'company': company,
                    'description': content,
                    # 'city': 1,
                    # 'language': 1,
                    # 'timestamp': 1,
                })
        else:
            errors.append({
                'url': url,
                'title': 'Div does not exists',
            })
    else:
        errors.append({
            'url': url,
            'title': 'Page do not response',
        })

    return jobs, errors



def hh(url):
    #   HH.RU
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', attrs={'class': 'vacancy-serp-content'})
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'serp-item'})
            for div in div_lst:
                title = div.find('span', attrs={'data-page-analytics-event': 'vacancy_search_suitable_item'})
                href = title.a['href']
                main_span_div = div.find('div', attrs={'class': 'g-user-content'})
                small_div_lst = main_span_div.find_all('div', attrs={'class': 'bloko-text'})
                content = ''
                for s_div in small_div_lst:
                    content += s_div.text
                    # The internal tag is ignored
                company = 'No name'
                name = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                if name:
                    company = name.text
                jobs.append({
                    'url': href,
                    'title': title.text,
                    'company': company,
                    'description': content,
                    # 'city': 1,
                    # 'language': 1,
                    # 'timestamp': 1,
                })
        else:
            errors.append({
                'url': url,
                'title': 'Div does not exists',
            })
    else:
        errors.append({
            'url': url,
            'title': 'Page do not response',
        })

    return jobs, errors



if __name__ == '__main__':
    url = 'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20'
    jobs, errors = hh(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))  # content is in bytes, and we need strings, so we convert
    h.close()   # https://realpython.com/python-requests/#content


