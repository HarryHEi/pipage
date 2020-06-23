from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from common.drf.pagination import CommonPagination

from .models import Book, Section, Content
from .serializers import BookSerializer, SectionSerializer, ContentSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CommonPagination


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    @action(methods=['GET'], detail=True)
    def get_next(self, request, **kwargs):
        section = self.get_object()
        next = section.book.sections.filter(index__gt=section.index).first()
        if next:
            return Response(
                data=SectionSerializer(instance=next).data
            )
        else:
            return Response(
                status=404
            )


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section']
