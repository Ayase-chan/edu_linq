from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Student
from api.serializers import StudentSerializer, StudentDeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from api.models import Book
from api.serializers import BookModelSerializerV2, BookModelSerializerV3


class StudentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print('get ok')
        std_id = kwargs.get('id')
        if std_id:
            std_obj = Student.objects.get(pk=std_id)
            std_serial = StudentSerializer(std_obj).data
            return Response({
                'status': 200,
                'message': '查询单个学生成功',
                'results': std_serial
            })
        else:
            std_all = Student.objects.all()
            std_data = StudentSerializer(std_all, many=True).data
            return Response({
                'status': 200,
                'message': '查询所有学生成功',
                'results': std_data,
            })

    def post(self, request, *args, **kwargs):
        print('post success')
        data = request.data
        print(data)
        # print(request.data['name'])
        if not isinstance(data, dict) or data == {}:
            return Response({
                "status": 400,
                "message": "参数有误",
            })
        s_data = StudentDeSerializer(data=data)
        # print(s_data)
        if s_data.is_valid():
            a = s_data.save()
            # print(type(a))
            return Response({
                'status': 200,
                'message': '添加成功',
                'results': StudentSerializer(a).data
            })
        else:
            return Response({
                'status': 400,
                'message': '添加失败',
                'results': s_data.errors
            })


class BookGenericAPIView(GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin):
    queryset = Book.objects.filter()
    serializer_class = BookModelSerializerV3

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class BookGenericAPIViewV3(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializerV3
    lookup_field = "id"




class BookViewSetView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializerV3

    def user_login(self, request, *args, **kwargs):
        request_data = request.data
        print("登录成功")
        return Response("登录成功")

    def get_user_count(self, request, *args, **kwargs):
        # 完成获取用户数量的逻辑
        print("查询成功")
        return self.list(request, *args, **kwargs)