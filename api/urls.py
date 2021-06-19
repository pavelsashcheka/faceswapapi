from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.GetAllUsers.as_view()),
    path('users/<int:pk>', views.GetSpecialUser.as_view()),
    path('process/', views.PostImage.as_view()),
    path('process/last', views.GetLastRecord.as_view()),
    path('process/<int:pk>', views.PostImage.as_view()),
]