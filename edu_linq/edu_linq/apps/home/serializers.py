from rest_framework.serializers import ModelSerializer

from home.models import Banner


class BannerModelSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ("img", "link", "title")


class NavigatorSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ("link", "title")
