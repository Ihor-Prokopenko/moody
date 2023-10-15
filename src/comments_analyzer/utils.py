from django.conf import settings
from urllib.parse import urlparse, parse_qs

from comments_analyzer.models import YoutubeVideo, YoutubeComment
from .serializers import YoutubeCommentSerializer

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY


class YoutubeVideoProcessor:
    video_model = YoutubeVideo
    comment_model = YoutubeComment
    api_key = YOUTUBE_API_KEY

    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = self.get_video_id()
        self.video_obj = self.get_or_create_video_obj()

    def get_or_create_video_obj(self):
        try:
            video_obj = self.video_model.objects.get(video_id=self.video_id)
        except self.video_model.DoesNotExist:
            video_obj = self.video_model.objects.create(youtube_url=self.video_url, video_id=self.video_id)
        return video_obj

    def get_video_id(self):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        query = urlparse(self.video_url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        return None

    def comments_to_db(self, comments_list: list):
        for comment in comments_list:
            youtube_id = comment.get("youtube_id")

            retrieve_comment, updated_or_created = self.comment_model.objects.update_or_create(
                youtube_id=youtube_id, video=self.video_obj,
                defaults={
                    "etag": comment.get("etag"),
                    "text": comment.get("text"),
                    "published_at": comment.get("published_at"),
                })
            if updated_or_created:
                # print(f"Comment was updated or created: {retrieve_comment.text}")
                retrieve_comment.processed = False
                retrieve_comment.save()
                # TODO: create task to process
                pass
        return True

    def request_comments(self, request_kwargs):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        try:
            results = youtube.commentThreads().list(**request_kwargs).execute()
        except HttpError as e:
            return None
        comments_list = []
        page_token = results.get("nextPageToken")
        for item in results['items']:
            comment_body = {
                "youtube_id": item['snippet']['topLevelComment']["id"],
                "text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
                "published_at": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                "etag": item["snippet"]["topLevelComment"]["etag"],
            }
            comments_list.append(comment_body)
        return comments_list, page_token

    def get_and_save_comments(self):
        page_token = None

        while True:
            req_kwargs = {
                "part": "snippet",
                "videoId": self.video_id,
                "textFormat": "plainText",
                "maxResults": 100,
                "pageToken": page_token,
            }
            comments, next_page = self.request_comments(request_kwargs=req_kwargs)
            self.comments_to_db(comments_list=comments)
            if next_page:
                page_token = next_page
                # print(f"Next page: id={next_page}")
                continue
            break

        return True

    def get_comments_list(self):
        try:
            result = self.video_model.objects.get(video_id=self.video_id).comments.all()
            serializer = YoutubeCommentSerializer(result, many=True)
            result = serializer.data
        except self.video_model.DoesNotExist:
            result = []
        return result




