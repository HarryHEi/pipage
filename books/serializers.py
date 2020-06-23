from rest_framework.serializers import ModelSerializer

from .models import Book, Section, Content


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
