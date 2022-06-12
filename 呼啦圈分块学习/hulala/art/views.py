# Create your views here.
import jwt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        exclude = ['author', ]  # 后台会自带session或者id传入，不用验证


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleDetail
        exclude = ['article', ]  # 文章验证成功后会生成id，无需传入


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'


class PageArticleSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        source='articledetail.content', required=False)
    author = serializers.CharField(source='author.username', required=False)
    category = serializers.CharField(
        source='get_category_display', required=False)

    class Meta:
        model = models.Article
        fields = '__all__'


class ArticleView(APIView):
    def get(self, request, *args, **kwargs):
        '''获取文章'''
        pk = kwargs.get('pk')
        if not pk:  # 获取概要
            condition = {}  # 筛选类别
            category = request.query_params.get('category')
            if category:
                condition['category'] = category
            queryset = models.Article.objects.filter(
                **condition).order_by('-date')
            page = PageNumberPagination()
            res = page.paginate_queryset(queryset, request, self)
            ser = ArticleListSerializer(instance=res, many=True)
            return Response(ser.data)

        article_obj = models.Article.objects.filter(id=pk).first()
        ser = PageArticleSerializer(instance=article_obj)
        return Response(ser.data)

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
        ser = ArticleSerializer(data=request.data)
        ser_detail = ArticleDetailSerializer(data=request.data)

        if ser.is_valid() and ser_detail.is_valid():
            article_obj = ser.save(author_id=1)
            ser_detail.save(article=article_obj)
            return Response('增加成功')

        return Response(ser.errors)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class OtherCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ['user', ]


class CommentView(APIView):
    def get(self, request, *args, **kwargs):
        '''评论列表，http://127.0.0.1:8000/art/comment/?article=1'''
        article_id = request.query_params.get('article')
        queryset = models.Comment.objects.filter(article_id=article_id)
        ser = CommentSerializer(instance=queryset, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        '''添加评论， 无需传入user，通过用户验证时，通过session自动获取'''
        '''
        http://127.0.0.1:8000/art/comment/
        {
            article:1,
            content:xxx,
        }
        '''

        ser = PostCommentSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user_id=1)
            return Response(ser.data)
        return Response(ser.errors)


class NewCommentView(ListAPIView, CreateAPIView):
    queryset = models.Comment.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['article', 'content', ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer
        elif self.request.method == "POST":
            return OtherCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author_id=1)

    # def get(self, request, *args, **kwargs):
    #     '''评论列表，http://127.0.0.1:8000/art/comment/?article=1'''
    #     article_id = request.query_params.get('article')
    #     queryset = models.Comment.objects.filter(article_id=article_id)
    #     ser = CommentSerializer(instance=queryset, many=True)
    #     return Response(ser.data)


class Login(APIView):
    '''通过用户名、密码登录，验证成功则生成token'''

    def post(self, request, *args, **kwargs):
        # 基于token的认证
        '''
        user = models.UserInfo.objects.filter(**request.data).first()
        if not user:
            return Response('登录失败')
        user.token = str(uuid.uuid4())
        user.save()
        return Response({'code':'1001','token':user.token})
        '''

        # 基于jwt的认证
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = models.UserInfo.objects.filter(**request.data).first()
        if not user:
            return Response({'code': 1000, 'error': '用户名或密码错误'})

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'code': '1001', 'token': token})


class Authication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token')
        # 减少数据库查询压力
        if not token:
            return (None, None)

        user = models.UserInfo.objects.filter(token=token).first()
        if user:
            # rest_framework 内部会将两个字段赋给 request, 以便后续使用
            # 分别为 self.user, self.auth
            return (user, token)
        return (None, None)

    def authenticate_header(self, request):
        '验证失败时，返回的响应头WWW-Authenticate对应的值'
        pass


class MyPermission(BasePermission):
    '''登录之后才可以评论，取评论不用验证'''
    message = {'status': False, 'error': '登录之后才可以评论'}

    def has_permission(self, request, view):
        if request.user:
            return True
        if request.method == "GET":
            return True
        return False


class Edit(APIView):
    authentication_classes = [Authication, ]

    def get(self, request, *args, **kwargs):
        if request.user:
            return Response('登录成功')
        return Response('登录失败')


class NewEdit(APIView):
    def get(self, request, *args, **kwargs):
        from rest_framework_jwt.settings import api_settings
        from rest_framework import exceptions
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        token = request.query_params.get('token')
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = "签名已过期"
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = '认证失败'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = '认证失败'
            raise exceptions.AuthenticationFailed(msg)

        print(payload)
        return Response('认证成功')
