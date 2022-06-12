from rest_framework.response import Response
from rest_framework.views import APIView


class OrderView(APIView):
    '''订单相关接口，都需要登录'''

    # authentication_classes = [auth.HulaQueryParamAuthentication]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('订单列表')

    def post(self, request, *args, **kwargs):
        return Response('创建订单')
