from rest_framework.generics import ListAPIView

from home.models import Banner, Navigator
from home.serializers import BannerModelSerializer, NavigatorSerializer


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_del=False).order_by("-orders")[:3]
    serializer_class = BannerModelSerializer


class NavigatorTopListAPIView(ListAPIView):
    queryset = Navigator.objects.filter(is_show=True, is_del=False, position=1).order_by("-orders")
    serializer_class = NavigatorSerializer


class NavigatorBottomListAPIView(ListAPIView):
    queryset = Navigator.objects.filter(is_show=True, is_del=False, position=2).order_by("-orders")
    serializer_class = NavigatorSerializer
