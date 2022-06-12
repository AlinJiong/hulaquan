# Create your views here.

from api import models
from api.extensions import auth
from api.serializer.comment import CommentCreateSerializers, CommentListSerializers

"""
from rest_framework.response import Response
from rest_framework.views import APIView

class CommentView(APIView):
    '''评论相关接口'''

    def get(self, request, *args, **kwargs):
        '''获取评论不用登录'''
        return Response('评论列表')

    def post(self, request, *args, **kwargs):
        '''发表评论需要登录'''
        return Response('发表评论')

    def get_authenticators(self):
        if self.request.method == "GET":
            return []
        # elif self.request.method == "POST":
        #     return [auth.HulaQueryParamAuthentication(), ]
"""

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.filters import BaseFilterBackend


class CommentFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        article_id = request.query_params.get('article', None)
        if not article_id:
            # 返回空的queryset
            return queryset.none()
        return queryset.filter(article_id=article_id)


class CommentView(ListAPIView, CreateAPIView):
    '''评论相关接口'''

    queryset = models.Comment.objects.all()
    filter_backends = [CommentFilterBackend, ]

    def get_authenticators(self):
        if self.request.method == "GET":
            return []
        elif self.request.method == "POST":
            return [auth.HulaQueryParamAuthentication(), ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentListSerializers
        return CommentCreateSerializers

    def perform_create(self, serializer):
        '''适用于保存comment，增加user数据'''
        print(self.request.user)
        serializer.save(user=self.request.user)
