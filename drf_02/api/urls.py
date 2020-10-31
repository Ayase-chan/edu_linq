from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from api import views

urlpatterns = [
    path('student/', views.StudentAPIView.as_view()),
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    path('student/<str:id>/', views.StudentAPIView.as_view()),
]
