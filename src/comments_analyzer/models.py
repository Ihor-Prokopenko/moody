from django.db import models


class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=255, blank=False, unique=True)
    youtube_url = models.CharField(max_length=255, blank=False)
    etag = models.CharField(max_length=255, blank=True)


class YoutubeComment(models.Model):
    video = models.ForeignKey(YoutubeVideo, on_delete=models.CASCADE, related_name="comments")
    youtube_id = models.CharField(max_length=255, blank=False, unique=True)
    etag = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    mood = models.BooleanField(null=True, default=None)
    published_at = models.DateTimeField()
    processed = models.BooleanField(default=False)


class AnalysisSession(models.Model):                                # TODO: COMPLETE
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    ready_to_report = models.BooleanField(null=False, default=False)

