from bs4 import BeautifulSoup
from tqdm import tqdm
from django.db.transaction import atomic

from common.http import sync_get
from books.logger import logger
from books.models import Book, Section, Content


HOME_URL = 'http://www.biquge.info'


class BpgSection:
    """一章"""
    def __init__(self, title, url):
        self.title = title
        self.url = url

        self.content = ''

        self._do_init()

    def save(self, book, index):
        with atomic():
            section = Section.objects.create(
                book=book,
                index=index,
                title=self.title,
            )
            Content.objects.create(
                section=section,
                body=self.content
            )

    def _do_init(self):
        res = sync_get(self.url)

        if res:
            soup = BeautifulSoup(res.content, features='html.parser')
            div_tags = soup.find_all(
                name='div',
                attrs={
                    'id': 'content'
                }
            )
            if div_tags:
                text = div_tags[0].text
                formatted_text = text.replace('\n\n', '').replace('\xa0\xa0\xa0\xa0', '\n').strip()
                self.content = formatted_text


class BpgBook:
    """一本书"""
    def __init__(self, title, home):
        self.title = title
        self.home_url = home

        self.sections = []

        self._do_init()

    def url_join(self, section_href):
        """获取文章链接"""
        if self.home_url.endswith('/'):
            return f'{self.home_url}{section_href}'
        else:
            return f'{self.home_url}/{section_href}'

    def save(self):
        book, _ = Book.objects.get_or_create(
            title=self.title
        )
        return book

    def _do_init(self):
        """获取每章连接"""
        logger.info(f'获取<{self.title}>主页')

        book = self.save()

        res = sync_get(self.home_url)
        if res:
            soup = BeautifulSoup(res.content, features='html.parser')
            div_tags = soup.find_all(
                name='div',
                attrs={
                    'id': 'list'
                }
            )
            if div_tags:
                a_tags = div_tags[0].find_all(name='a')
                for index, a_tag in tqdm(enumerate(a_tags)):
                    href = a_tag.get('href')
                    title = a_tag.text
                    section = BpgSection(title, self.url_join(href))
                    section.save(book, index + 1)
                    self.sections.append(section)
