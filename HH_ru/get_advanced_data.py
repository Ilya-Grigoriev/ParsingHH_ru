import json
import time

import requests
from loguru import logger
from typing import List

logger.add('data.log')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}


def get_area_id(region: str) -> int:
    url = f'https://kazan.hh.ru/autosuggest/multiprefix/v2?d=areas_RU&q={region}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['items'][0]['id']


def get_ids(url: str, obj: str) -> List[str]:
    response = requests.get(url, headers=headers)
    if response == 200:
        ind = int(obj.split('. ')[0]) - 1
        items = response.json()['items'][ind]['items']
        return [item['id'] for item in items]


def get_vacancies(keywords: str = '', count_pars: int = 1, role: str = '',
                  indust: str = '', region: str = 'Москва',
                  income: int = 0, cur: str = 'RUB',
                  exp: str = 'Не имеет значения', busy: List[str] = None,
                  graph: List[str] = None, sort: str = 'По соответствию',
                  output: str = 'За всё время', path: str = 'C:/'):
    formatted_exp = {
        'Не имеет значения': 'doesNotMatter',
        'Нет опыта': 'noExperience',
        'От 1 года до 3 лет': 'between1And3',
        'От 3 до 6 лет': 'between3And6',
        'Больше 6': 'moreThan6'
    }
    formatted_busy = {
        'Полная': 'full',
        'Частичная': 'part',
        'Волонтёрство': 'volunteer',
        'Стажировка': 'probation'
    }
    formatted_graph = {
        'Полный': 'fullDay',
        'Сменный': 'shift',
        'Гибкий': 'flexible',
        'Удалённый': 'remote',
        'Вахтовый метод': 'flyInFlyOut'
    }
    formatted_sort = {
        'По соответствию': 'relevance',
        'По дате изменения': 'publication_time',
        'По убыванию зарплат': 'salary_desc',
        'По возрастанию зарплаты': 'salary_asc'
    }
    formatted_output = {
        'За всё время': '0',
        'За месяц': '30',
        'За неделю': '7',
        'За последние три дня': '3',
        'За сутки': '1'
    }
    data = dict()
    logger.info('Start get area id')
    area = get_area_id(region)
    logger.info('End get area id')
    if area:
        data['area'] = area
    data['text'] = '+'.join(keywords.split())

    if role:
        url = 'https://hh.ru/shards/professional_role?lang=RU'
        logger.info('Start get ids for spec')
        spec_ids = get_ids(url, role)
        logger.info('End get ids for spec')
        if spec_ids:
            formatted_role = '&'.join(
                [f'professional_role={id}' for id in spec_ids])
            data['professional_role'] = formatted_role

    if indust:
        url = 'https://hh.ru/shards/industry?lang=RU&site=12&useParentId=true'
        logger.info('Start get ids for branch')
        branch_ids = get_ids(url, indust)
        logger.info('End get ids for branch')
        if branch_ids:
            formatted_indust = '&'.join(
                [f'industry={id}' for id in branch_ids])
            data['industry'] = formatted_indust

    data['salary'] = income
    data['currency_code'] = cur
    data['experience'] = formatted_exp[exp]

    if busy:
        data['employment'] = '&'.join(
            [f'employment={formatted_busy[i]}' for i in busy])
    if graph:
        data['schedule'] = '&'.join(
            [f'schedule={formatted_graph[i]}' for i in graph])
    if sort:
        data['order_by'] = formatted_sort[sort]
    if output:
        data['search_period'] = formatted_output[output]

    sample_url = 'https://hh.ru/search/vacancy?no_magic=true'
    for key, value in data.items():
        sample_url += '&' + key + '=' + str(value)

    urls = [sample_url + f'&page={page_n}' for page_n in range(0, count_pars)]
    file = open('data.json', mode='w', encoding='utf-8')
    json.dump({'urls': urls, 'error': False, 'path': path} if urls else {
        'error': True}, file)


if __name__ == '__main__':
    start = time.time()
    get_vacancies('', 1, '1. Автомобильный бизнес', '1. Автомобильный бизнес',
                  'Москва', 100, 'USD', 'Нет опыта', ['Полная', 'Частичная'],
                  ['Полный', 'Сменный'], 'По убыванию зарплат', 'За месяц',
                  r'C:\\')
    logger.info(f'Total time: {time.time() - start}')
