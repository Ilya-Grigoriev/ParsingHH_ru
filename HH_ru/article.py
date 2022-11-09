import json
import os

import scrapy_splash
from scrapy_splash import SplashRequest
import scrapy
from project import main_for_project


class ArticleSpider(scrapy.Spider):
    name = 'article'

    def __init__(self) -> None:
        self.list_data = []
        self.path = None

    def start_requests(self) -> scrapy_splash.SplashRequest:
        main_for_project()
        file = json.load(open('data.json', encoding='utf-8'))
        start_urls = file['urls']
        self.path = file['path']
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
        for url in start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5},
                                headers=headers)

    def parse(self, response: scrapy.http.Response) -> None:
        if response.xpath('//div[@class="vacancy-serp-content"]'):
            items = response.xpath('//div[@class="serp-item"]')
            for item in items:
                title = item.css('a.serp-item__title::text').get()
                url = item.css('a.serp-item__title').xpath('@href').get()
                company = ''.join(
                    item.css('a.bloko-link_kind-tertiary::text').getall())
                salary = ''.join(
                    item.css('span.bloko-header-section-3::text').getall())
                city = item.css(
                    'div[data-qa="vacancy-serp__vacancy-address"]::text').get()
                data = dict()
                data['Title'] = title.replace(' ', ' ').replace(' ', ' ')
                data['URL'] = url.replace(' ', ' ').replace(' ', ' ')
                data['Company'] = company.replace(' ', ' ').replace(' ',
                                                                    ' ') if company else 'None'
                data['Salary'] = salary.replace(' ', ' ').replace(' ',
                                                                  ' ') if salary else 'None'
                data['City'] = city.replace(' ', ' ').replace(' ',
                                                              ' ') if city else 'None'
                self.list_data.append(data)

    def close(spider: scrapy.Spider, reason) -> None:
        path = os.path.dirname(spider.path)
        total_path = os.path.join(path, 'scraping_data.json')
        file = open(total_path, mode='w', encoding='utf-8')
        json.dump(spider.list_data, file, ensure_ascii=False)
        file.close()
