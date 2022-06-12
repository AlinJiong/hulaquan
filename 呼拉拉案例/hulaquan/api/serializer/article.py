from rest_framework import serializers

from api import models


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    category = serializers.CharField(source='get_category_display')
    date = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = '__all__'

    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S') if obj.date else ""


class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        exclude = ['author', ]  # 后台会自带session或者id传入，不用验证


class ArticleDetailSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleDetail
        exclude = ['article', ]  # 文章验证成功后会生成id，无需传入


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    category = serializers.CharField(source='get_category_display')
    date = serializers.SerializerMethodField(required=False)
    content = serializers.CharField(source='articledetail.content')

    class Meta:
        model = models.Article
        fields = '__all__'

    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S') if obj.date else ""
