from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from .utils import get_comments_from_youtube

# Create your views here.


# def get_comments(request):
#
#     res = get_comments_from_youtube()
#
#     return Response(res, status=status.HTTP_200_OK)


class CommentsAPIView(APIView):

    @staticmethod
    def get(request):
        res = get_comments_from_youtube()
        response_data = {
            "message": res,
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        return response
