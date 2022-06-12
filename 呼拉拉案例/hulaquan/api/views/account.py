# Create your views here.
from api import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = models.UserInfo.objects.filter(**request.data).first()
        # 1、根据用户名和密码判断是否可以登录
        if not user:
            return Response({'code': 1001, 'msg': '用户名或密码错误！'})
        # 2、根据用户生成payload中间数据
        payload = jwt_payload_handler(user)
        # 3、生成token
        token = jwt_encode_handler(payload)
        return Response({'code': '1000', 'token': token})
