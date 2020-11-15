from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
    path("phone/", views.MobileCheckAPIView.as_view()),
    path("send/", views.SendMessageAPIView.as_view()),
    path("login_2/", views.UserAPIViewV2.as_view()),
]
