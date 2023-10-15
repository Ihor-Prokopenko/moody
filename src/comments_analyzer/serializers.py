from rest_framework import serializers

from .models import YoutubeComment


class YoutubeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeComment
        fields = ["youtube_id", "etag", "text", "mood", "published_at"]
