from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=64, verbose_name='书名')
    cover = models.CharField(max_length=256, default='', blank=True)

    def __str__(self):
        return f'Book({self.title})'

    def __repr__(self):
        return f'<{self}>'


class Section(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='sections')
    index = models.FloatField(verbose_name='章节序号')
    title = models.CharField(max_length=64, verbose_name='章节名称')

    def __str__(self):
        return f'Section({self.title})'

    def __repr__(self):
        return f'<{self}>'


class Content(models.Model):
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='contents')
    body = models.TextField(default='', verbose_name='文本内容')

    def __str__(self):
        return f'Content({self.id})'

    def __repr__(self):
        return f'<{self}>'
