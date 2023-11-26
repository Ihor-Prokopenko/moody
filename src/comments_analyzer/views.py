from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from .utils import YoutubeVideoProcessor


class CommentsAPIView(APIView):

    @staticmethod
    def get(request):
        # dummy_link = "https://www.youtube.com/watch?v=ZDTJDZNUfwA"
        dummy_link = "https://www.youtube.com/watch?v=-tg4BR-BPO0"

        video_processor = YoutubeVideoProcessor(video_url=dummy_link)

        video_processor.get_and_save_comments()

        comments = video_processor.get_comments_list()

        response_data = {
            "comments_count": len(comments),
            "comments": comments,
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        return response
