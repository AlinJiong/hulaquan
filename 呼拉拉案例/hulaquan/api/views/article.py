# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.throttling import AnonRateThrottle

from api import models
from api.serializer.article import ArticleSerializer, ArticlePostSerializer, ArticleDetailSaveSerializer, \
    ArticleDetailSerializer


class ArticleView(ListAPIView):
    '''文章相关接口，无需登录就可以查看'''

    authentication_classes = []
    throttle_classes = [AnonRateThrottle, ]

    queryset = models.Article.objects.all()
    serializer_class = ArticleSerializer

    # def get(self, request, *args, **kwargs):
    #     '''文章列表 && 文章详细'''
    #     return Response('无需认证')

    def post(self, request, *args, **kwargs):
        '''新增文章，应该在后台管理开发实现'''
        '''http://127.0.0.1:8000/art/article/
        {
            "category":1,
            "title":"新闻",
            "image":"xxx",
            "summary":"简介",
            "content":"内容"
        }
        无需传入user，通过用户验证时，通过session自动获取
        '''
        ser = ArticlePostSerializer(data=request.data)
        ser_detail = ArticleDetailSaveSerializer(data=request.data)

        if ser.is_valid() and ser_detail.is_valid():
            article_obj = ser.save(author_id=1)
            ser_detail.save(article=article_obj)
            return Response('增加成功')

        return Response(ser.errors)


class ArticleDetailView(RetrieveAPIView):
    authentication_classes = []
    queryset = models.Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get(self, request, *args, **kwargs):
        '''增加浏览数，在原有的get方法新加功能'''
        res = super().get(request, *args, **kwargs)
        pk = kwargs.get('pk')
        from django.db.models import F
        models.Article.objects.filter(pk=pk).update(read_count=F('read_count') + 1)

        # instance = self.get_object() # 返回对象
        # instance.read_count += 1
        # instance.save()
        return res


"""
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet
from api.serializer.article import ArticleSerializer, ArticleDetailSerializer


class ArticleView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    authentication_classes = []
    throttle_classes = [AnonRateThrottle, ]
    queryset = models.Article.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        # if self.request.method == 'POST':
        #     return ArticlePostSerializer
        pk = self.kwargs.get('pk')
        if pk:
            return ArticleDetailSerializer
        return ArticleSerializer

    def create(self, request, *args, **kwargs):
        '''增加文章'''
        pass
"""
