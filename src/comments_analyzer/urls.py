from django.urls import path

from .utils import get_comments_from_youtube

from .views import CommentsAPIView


urlpatterns = [
    path('comments/', CommentsAPIView.as_view(), name="comments"),

    ]
