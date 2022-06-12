from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import models


class CategoryView(APIView):
    def post(self, request, *args, **kwargs):
        # print(request.body)
        # print(request.POST)
        # print(request.POST.get('name'))
        # print(request.data)

        models.Category.objects.create(**request.data)
        return Response('Ok')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = models.Category.objects.filter(pk=pk).first()
            data = model_to_dict(obj)
            return Response(data)

        data = models.Category.objects.all().values('id', 'name')
        print(data)
        return Response(data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        models.Category.objects.filter(pk=pk).delete()
        return Response("删除成功")

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        models.Category.objects.filter(pk=pk).update(**request.data)
        return Response('更新成功！')


class NewCatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        # fields = "__all__"
        fields = ['id', 'name']


class NewCatagoryView(APIView):
    '''
    加上serializer验证
    '''

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = models.Category.objects.filter(pk=pk).first()
            # 序列化的数据，instance传入
            ser = NewCatagorySerializer(instance=obj)
            return Response(ser.data)
        else:
            obj = models.Category.objects.all()
            ser = NewCatagorySerializer(instance=obj, many=True)
            return Response(ser.data)

    def post(self, request, *args, **kwargs):
        # 反序列化数据，data传入
        ser = NewCatagorySerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = models.Category.objects.filter(pk=pk).first()
        # 修改数据，两者均传入
        ser = NewCatagorySerializer(instance=obj, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def patch(self, request, *args, **kwargs):
        '''
        局部更新，partial=True
        '''
        pk = kwargs.get('pk')
        obj = models.Category.objects.filter(pk=pk).first()
        # 修改数据，两者均传入
        ser = NewCatagorySerializer(
            instance=obj, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        models.Category.objects.filter(pk=pk).delete()
        return Response("删除成功")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class TagView(ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name', required=False)
    tag_name = serializers.SerializerMethodField(required=False)

    class Meta:
        model = models.Article
        fields = '__all__'
        # depth = 1

    def get_tag_name(self, row):
        tags = row.tag.all()
        res = []
        for tag in tags:
            res.append(tag.label)
        return res


class GetArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'


class Article(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = models.Article.objects.filter(pk=pk).first()
            # 序列化的数据，instance传入
            ser = GetArticleSerializer(instance=obj)
            return Response(ser.data)
        else:
            obj = models.Article.objects.all()
            print(obj)
            ser = GetArticleSerializer(instance=obj, many=True)
            return Response(ser.data)

    def post(self, request, *args, **kwargs):
        # 反序列化数据，data传入
        print(request.data)
        ser = ArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)

    def put(self, request, *args, **kwargs):
        '''
        全部更新，全部字段都需要传
        '''
        pk = kwargs.get('pk')
        obj = models.Article.objects.filter(pk=pk).first()
        # 修改数据，两者均传入
        ser = ArticleSerializer(instance=obj, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def patch(self, request, *args, **kwargs):
        '''
        局部更新，partial=True
        '''
        pk = kwargs.get('pk')
        obj = models.Article.objects.filter(pk=pk).first()
        # 修改数据，两者均传入
        ser = ArticleSerializer(instance=obj, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        models.Article.objects.filter(pk=pk).delete()
        return Response("删除成功")


class MyPagination(PageNumberPagination):
    page_size = 2  # 每个页面默认显示个数
    page_size_query_param = 'size'  # 调节每个页面的显示个数
    max_page_size = 4
    page_query_param = 'page'  # 调节跳转页码


class PageArticle(APIView):
    def get(self, request, *args, **kwargs):
        queryset = models.Article.objects.all()
        pg = PageNumberPagination()
        res = pg.paginate_queryset(queryset, request, self)
        ser = GetArticleSerializer(instance=res, many=True)
        return Response(ser.data)
