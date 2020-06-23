from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import UserInfoViewSet, LogoutView


router = DefaultRouter()
router.register('user_info', UserInfoViewSet, basename='user_info')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
