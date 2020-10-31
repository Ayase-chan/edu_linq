from django.urls import path, include
from drf_app import views
urlpatterns = [
    path('users/', views.login),
    path('user_view/', views.UserView.as_view()),
    path("student/", views.StudentAPIView.as_view())
]
