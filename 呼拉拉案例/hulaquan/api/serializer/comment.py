from rest_framework import serializers

from api import models


class CommentListSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = models.Comment
        fields = '__all__'


class CommentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ['user', ]
