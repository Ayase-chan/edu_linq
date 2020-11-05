from django.urls import path
from home import views

urlpatterns = [
    path("banner/", views.BannerListAPIView.as_view()),
    path("navigator_top/", views.NavigatorTopListAPIView.as_view()),
    path("navigator_bot/", views.NavigatorBottomListAPIView.as_view()),
]
