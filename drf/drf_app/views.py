from django.http import HttpResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView


def login(request):
    return HttpResponse("ok")


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request, *args, **kwargs):
        print("get query")
        return HttpResponse('get ok')

    def post(self, request, *args, **kwargs):
        print("post query")
        return HttpResponse('post ok')


class StudentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print('gtk')
        return Response("drf get ok")

    def post(self, request, *args, **kwargs):
        print('post ok')
        return Response("drf post ok")
