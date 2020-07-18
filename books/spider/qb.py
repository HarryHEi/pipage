import time

from bs4 import BeautifulSoup
from tqdm import tqdm
from django.db.transaction import atomic

from common.http import sync_get
from books.logger import logger
from books.models import Book, Section, Content


HOME_URL = 'http://www.biquge.info'


class QbSection:
    """一章"""
    def __init__(self, title, url):
        self.title = title
        self.url = url

        self.content = ''

        self._do_init()

    @staticmethod
    def is_exists(book, index):
        try:
            section = Section.objects.get(
                book=book,
                index=index,
            )
        except Section.DoesNotExist:
            return False

        content = section.contents.first()
        if content and content.body:
            return True

        return False

    def save(self, book, index):
        with atomic():
            section, _ = Section.objects.get_or_create(
                book=book,
                index=index,
                title=self.title,
            )
            content, _ = Content.objects.get_or_create(
                section=section,
                defaults={
                    'body': self.content
                }
            )
            if content.body == '' and self.content:
                content.body = self.content
                content.save()

    def _do_init(self):
        for _ in range(5):
            res = sync_get(self.url)

            if res:
                soup = BeautifulSoup(res.content, features='html.parser')
                div_tags = soup.find_all(
                    name='div',
                    attrs={
                        'id': 'mlfy_main_text'
                    }
                )
                if div_tags:
                    text = div_tags[0].text
                    formatted_text = text.replace('\n\n', '').replace('\xa0\xa0\xa0\xa0', '\n').strip()
                    if formatted_text:
                        self.content = formatted_text
                        break
                    else:
                        time.sleep(1)


class QbBook:
    url_root = 'https://www.x23qb.com'

    """一本书"""
    def __init__(self, title, book_id):
        self.title = title
        self.home_url = f'{self.url_root}/book/{book_id}/'

        self._do_init()

    def url_join(self, section_href):
        """获取文章链接"""
        return f'{self.url_root}{section_href}'

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
                name='ul',
                attrs={
                    'id': 'chapterList'
                }
            )
            if div_tags:
                a_tags = div_tags[0].find_all(name='a')
                for index, a_tag in tqdm(enumerate(a_tags)):
                    href = a_tag.get('href')
                    title = a_tag.text
                    if not QbSection.is_exists(book, index + 1):
                        section = QbSection(title, self.url_join(href))
                        section.save(book, index + 1)
