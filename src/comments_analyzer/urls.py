from django.urls import path

from .views import CommentsAPIView


urlpatterns = [
    path('comments/', CommentsAPIView.as_view(), name="comments"),

    ]
