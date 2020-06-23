from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, SectionViewSet, ContentViewSet


router = DefaultRouter()
router.register('book', BookViewSet)
router.register('section', SectionViewSet)
router.register('content', ContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
