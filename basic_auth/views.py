from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class UserInfoViewSet(GenericViewSet, mixins.ListModelMixin):
    """用户查询自己的信息"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user

        return Response({
            'id': user.id,
            'username': user.username,
            'name': user.last_name + user.first_name,
            'admin': user.is_superuser,
        })


class LogoutView(APIView):
    """登出"""
    def post(self, request, *args, **kwargs):
        user = self.request.user

        if user:
            response = Response({
                'id': user.id,
                'username': user.username,
            })
        else:
            response = Response({
                'id': None,
                'username': 'stranger',
            })

        return response
